from copy import copy

from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
import Acquisition

from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.app.portlets.portlets import base
from plone.memoize import ram
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from osha.policy.adapter.subtyper import IAnnotatedLinkList
from osha.theme.vocabulary import AnnotatableLinkListVocabulary

class IPracticalSolutionsPortlet(IPortletDataProvider):
    pass

class Assignment(base.Assignment):

    implements(IPracticalSolutionsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return "Practical Solutions"

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('practical_solutions.pt')
    sections = ['useful-links',
                'risk-assessment-tools',
                'case-studies',
                'providers',
                'faqs']

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context,
                                 'portal_languages').getPreferredLanguage()
        return (preflang)

    #@ram.cache(_render_cachekey)
    def render(self):
        return self._template()

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = self.context

    def getBrainsBySection(self, brains, brains_per_section):
        """
        Return a number of brains for each section.

        To avoid doing a separate catalog query for each section the
        results of a single query for all Practical Solutions are
        filtered through this method by their portal_type to return a
        dictionary: {section: [brain0, brain1]}

        brains_per_section determines the number of brains to be
        returned for each section.
        """

        # The dictionary to collect the results
        section_brain_map = {}
        # Initialise the dictionary with empty lists
        for section in self.sections:
            section_brain_map[section] = []
        # A map from portal_types of the brains to sections
        portal_types_section_map = {'OSH_Link' : 'useful-links',
                                    'RALink' : 'risk-assessment-tools',
                                    'CaseStudy' : 'case-studies',
                                    'Provider' : 'providers',
                                    'File' : 'faqs'}
        # Loop through the brains filling up the section_brain_map
        # until there are the number specified in brains_per_section
        # of brains for each section. Sections are removed from
        # sections_to_be_mapped until it is empty.
        sections_to_be_mapped = copy(self.sections)
        # In case something goes wrong, i.e. not enough results are
        # found for a particular section after trying 500 brains then
        # just return what has been collected so far.
        limit = 500
        for brain in brains:
            limit -= 1
            pt = brain.portal_type
            section = portal_types_section_map[pt]
            if section in sections_to_be_mapped:
                section_brain_map[section].append(brain)
                if len(section_brain_map[section]) == brains_per_section:
                    sections_to_be_mapped.remove(section)
            if len(sections_to_be_mapped) == 0 or limit == 0:
                # If there are no remaining sections to be mapped or
                # the limit has been reached break out of the loop
                break
        return section_brain_map

    def getRecentPracticalSolutions(self):
        context = Acquisition.aq_inner(self.context)
        search_portal_types = [ "OSH_Link", "RALink", "CaseStudy", "Provider"]
        # Publications are Files which implement the
        # IPublicationEnhanced interface
        query = ( Eq('portal_type', 'File') & \
                      Eq('object_provides',
                         'slc.publications.interfaces.IPublicationEnhanced')
                  )
        query = Or(query,
                   In('portal_type', search_portal_types)
                   ) & Eq('review_state','published')
        pc = getToolByName(context, 'portal_catalog')
        if hasattr(pc, 'getZCatalog'):
            pc = pc.getZCatalog()
        brains = pc.evalAdvancedQuery(query, (('effective','desc'),))
        results = self.getBrainsBySection(brains, 3)
        return results

    def getLocalisedSectionTitles(self):
        """ In the Practical Solutions area there are
        captions under the images for each section. These are derived from
        the section folder Title.

        We could look up these Titles to get localised section Titles
        here too, but this method uses the standard plone language
        tools instead, perhaps the Practical Solutions area should use
        these translations too.
        """

        context = self.context
        trans_tool = getToolByName(context, "translation_service")
        lang_tool = getToolByName(context, "portal_languages")
        language = lang_tool.getPreferredLanguage()
        section_title_map = {}

        for section in self.sections:
            # convert "useful-links" to "heading_useful_links"
            msgid = "heading_%s" % section.replace("-", "_")
            section_title_map[section] = \
                trans_tool.utranslate("osha",
                                      msgid,
                                      {},
                                      context=context,
                                      target_language=language,
                                      default=section)
        return section_title_map

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IPracticalSolutionsPortlet)

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IPracticalSolutionsPortlet)

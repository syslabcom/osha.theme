from copy import copy

from zope.app.form.browser import MultiCheckBoxWidget
from zope.component import getMultiAdapter
from zope.formlib import form
from zope import schema
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
    subject = schema.List(
                    title=_(u"Categories"),
                    description=_(u"Please select a relevant category for the "
                    "items in this portlet. This should match the section "
                    "category."),
                    required=True,
                    value_type=schema.Choice(
                        vocabulary="osha.theme.SubjectValuesVocabulary"),
                    )


class Assignment(base.Assignment):

    implements(IPracticalSolutionsPortlet)

    def __init__(self, subject):
        self.subject = subject

    @property
    def title(self):
        return "Practical Solutions"


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('practical_solutions.pt')
    sections = ['publications',
                'case-studies',
                'useful-links',
                'faqs',
                'risk-assessment-tools',
                'providers']

    portal_types_map = {
            "useful-links":"OSH_Link",
            "risk-assessment-tools":"RALink",
            "case-studies":"CaseStudy",
            "providers":"Provider",
            "faqs":"FAQs",
            "publications": "Publication"
            }

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

    def get_more_url(self, section):
        """
        Return a url to more search results for a section
        """
        language = getToolByName(self.context,
                                 'portal_languages').getPreferredLanguage()
        subsection = self.portal_types_map[section]
        url = "db_filter?search_portal_types:list=%s&getRemoteLanguage=%s" \
              %(subsection, language)
        return url

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
                                    'File' : 'publications',
                                    'Faq' : 'faqs'}
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

    def getRecentPublications(self):
        """ Return 3 recent publications. This was the result of a
        last minute change to just show publications rather than
        Practical Solutions.
        """

        context = Acquisition.aq_inner(self.context)
        subject = self.data.subject
        search_portal_types = ["Publication"]
        # Publications are Files which implement the
        # IPublicationEnhanced interface
        query = ( Eq('portal_type', 'File') & \
                      Eq('object_provides',
                         'slc.publications.interfaces.IPublicationEnhanced') & \
                      In('Subject', subject)
                  )
        query = Or(query,
                   In('portal_type', search_portal_types)
                   ) & Eq('review_state','published')
        pc = getToolByName(context, 'portal_catalog')
        if hasattr(pc, 'getZCatalog'):
            pc = pc.getZCatalog()
        brains = pc.evalAdvancedQuery(query, (('effective','desc'),))
        results = brains[:3]
        return results

    def getDBFilterQueryString(self, practical_solution):
        """ Construct the query string for db_filter with the relevant
        language, database and keywords"""
        context = self.context
        subjects = self.data.subject
        keyword_query = ["&keywords:list="+i for i in subjects][0]
        preflang = getToolByName(context,
                                 'portal_languages').getPreferredLanguage()
        database = ""
        if self.portal_types_map.has_key(practical_solution):
            database = self.portal_types_map[practical_solution]
        query_string = "language=%s&search_portal_types:list=%s%s" \
              %(preflang, database, keyword_query)
        return query_string

    def getDBFilterURL(self, practical_solution):
        context = self.context
        portal_url = getToolByName(context, 'portal_url')()
        preflang = getToolByName(context,
                                 'portal_languages').getPreferredLanguage()
        query_string = self.getDBFilterQueryString(practical_solution)
        url = "%s/%s/db_filter?%s"\
              %(portal_url, preflang, query_string)
        return url

    def getPracticalSolutionsURL(self, practical_solution):
        """ Construct the url for links to the practical solution page
        of filtered results according to language.
        """
        context = self.context
        portal_url = getToolByName(context, 'portal_url')()
        preflang = getToolByName(context,
                                 'portal_languages').getPreferredLanguage()
        query_string = self.getDBFilterQueryString(practical_solution)
        url = "%s/%s/practical-solutions/%s?%s"\
              %(portal_url, preflang, practical_solution, query_string)
        return url

    def getRecentPracticalSolutions(self):
        context = self.context
        subject = self.data.subject
        search_portal_types = [ "OSH_Link", "RALink",
                                "CaseStudy", "Provider", "Publication"]
        # Publications are Files which implement the
        # IPublicationEnhanced interface
        query = ( Eq('portal_type', 'File') & \
                      Eq('object_provides',
                         'slc.publications.interfaces.IPublicationEnhanced') & \
                      In('Subject', subject)
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

def MultiCheckBoxWidgetFactory(field, request):
    """ Factory method to create MultiCheckBoxWidgets """
    return MultiCheckBoxWidget(
        field, field.value_type.vocabulary, request)


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    form_fields = form.Fields(IPracticalSolutionsPortlet)
    form_fields['subject'].custom_widget  = MultiCheckBoxWidgetFactory

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IPracticalSolutionsPortlet)
    form_fields['subject'].custom_widget  = MultiCheckBoxWidgetFactory

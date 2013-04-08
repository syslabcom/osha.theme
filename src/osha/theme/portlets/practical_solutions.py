from copy import copy

import Acquisition

from zope.formlib import form
from zope import schema
from zope.interface import implements
from zope.i18n import translate
from zope.app.form.browser import MultiCheckBoxWidget

from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets.portlets import base

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from osha.theme.browser.utils import search_solr

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
            "faqs":"HelpCenterFAQ",
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

    def getMorePublicationsUrl(self):
        """
        Construct the link to more publications for this section.
        """
        context = self.context
        preflang = getToolByName(context,
                                 'portal_languages').getPreferredLanguage()
        portal_url = getToolByName(context, 'portal_url')()
        subjects = self.data.subject
        keyword_query = "&Subject:list=".join(subjects)
        url = "%s/%s/publications/publications-overview?Subject:list=%s"\
              %(portal_url, preflang, keyword_query)
        return url

    def getBrainsBySection(self, brains, brains_per_section):
        """
        NOTE: this was no longer required for the portlet, but may be
        used again in the future


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
        lang = self.context.portal_languages.getPreferredLanguage()
        # Publications are Files which implement the
        # IPublicationEnhanced interface
        # query = ( Eq('portal_type', 'File') & \
        #               Eq('object_provides',
        #                  'slc.publications.interfaces.IPublicationEnhanced') & \
        #               In('Subject', subject)
        #           )
        # query = query & Eq('review_state','published')
        # if lang == "en":
        #     query = query & In('Language', [lang, ""])
        # else:
        #     query = query & Eq('Language', lang)
        # brains = pc.evalAdvancedQuery(query, (('effective','desc'),))

        query = {
            'portal_type': 'File',
            'object_provides': 'slc.publications.interfaces.IPublicationEnhanced',
            'Subject': subject,
            'review_state': 'published',
            'sort_on': 'effective',
            'sort_order': 'descending',
        }

        if lang == "en":
            query['Language'] = [lang, ""]
        else:
            query['Language'] = [lang, ""]

        pc = getToolByName(context, 'portal_catalog')
        if hasattr(pc, 'getZCatalog'):
            pc = pc.getZCatalog()
        brains = pc(query)
        results = brains[:3]
        return results

    def getPracticalSolutionsURL(self, practical_solution):
        """ Construct the url for links to the practical solution page
        of filtered results according to language.
        """
        context = self.context
        subjects = self.data.subject
        portal_url = getToolByName(context, 'portal_url')()
        preflang = getToolByName(
            context, 'portal_languages').getPreferredLanguage()
        keyword_query = ["keywords:list="+i for i in subjects][0]
        if practical_solution == "faqs":
            subject = subjects and subjects[0] or ""
            url = ("%s/%s/faq/osha_help_center_view?SearchableText="
                   "&category=%s" %(portal_url, preflang, subject))
        else:
            url = ("%s/%s/practical-solutions/%s?%s#database_search" %(
                    portal_url, preflang, practical_solution, keyword_query))
        return url

    def getRecentPracticalSolutions(self):
        context = self.context
        subject = self.data.subject
        search_portal_types = [ "OSH_Link", "RALink",
                                "CaseStudy", "Provider", "Publication"]
        # Publications are Files which implement the
        # IPublicationEnhanced interface
        query = '((portal_type:File ' \
                'AND object_provides:slc.publications.interfaces.IPublicationEnhanced ' \
                'AND Subject:(%(Subject)s)) ' \
            'OR ' \
                'portal_type:(%(portal_type)s)) ' \
          'AND ' \
            'review_state:published' % {
                        'Subject': subject,
                        'portal_type': search_portal_types,
                            }
        brains = search_solr(query, sort='effective desc')
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
        lang_tool = getToolByName(context, "portal_languages")
        language = lang_tool.getPreferredLanguage()
        section_title_map = {}

        for section in self.sections:
            # convert "useful-links" to "heading_useful_links"
            msgid = "heading_%s" % section.replace("-", "_")
            section_title_map[section] = \
                translate(domain="osha",
                              msgid=msgid,
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

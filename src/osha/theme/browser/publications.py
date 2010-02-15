from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
import Acquisition
from zope.component import getMultiAdapter
from DateTime import DateTime

class PublicationsSearchView(BrowserView):
    """View for displaying the publications overview page at /xx/publications
    """
    template = ViewPageTemplateFile('templates/publicationsearch.pt')
    template.id = "publications-overview"

    def __call__(self):
        self.request.set('disable_border', True)

        return self.template()

    def get_subject(self):
        subject = self.request.get('Subject', '')
        if subject == ['']:
            subject = ''
        #subject = [x.encode('utf-8') for x in subject]
        return subject

    def make_query(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        query = {'portal_type': 'File',
                 'object_provides': 'slc.publications.interfaces.IPublicationEnhanced',
                 'path': navigation_root_path,
                 'sort_on': 'effective',
                 'sort_order':'reverse'}
        if self.get_subject():
            query.update({'Subject': self.get_subject()})

        st = self.request.get('SearchableText' '')
        if st:
            query.update({'SearchableText': st})
        return query

    def get_link_to_english_results(self):
        """
        If the selected language is not English, then return a link to
        the equivalent search results in English
        """
        preflang = getToolByName(self.context,
                                 'portal_languages').getPreferredLanguage()
        url = ""
        if preflang != "en":
            solution = self.aq_parent.getCanonical().absolute_url()
            keywords = self.request.get("Subject", "")
            if keywords != [""]:
                keywords = keywords[0]
            url = "%s?Subject:list=%s"\
                  % (solution, keywords)
        return url


class QuestionsInParliamentSearchView(BrowserView):
    """ View for displaying the publications search page for Questions In Parliament on BeSWIC.be
    """
    template = ViewPageTemplateFile('templates/questionsinparliamentsearch.pt')
    template.id = "questions-in-parliament-search"

    def __call__(self):
        self.request.set('disable_border', True)

        return self.template()

    def getImageSrc(self):
        # look for a local image
        if getattr(Acquisition.aq_base(self.context), 'questions.gif', None):
            return "questions.gif"
        # return the default
        return "publications.gif"

    def getIntro(self):
        if getattr(Acquisition.aq_base(self.context), 'intro', None):
            return getattr(self.context, 'intro').getText()
        return ""

    def make_query(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        query = dict(portal_type ='File',
                 object_provides = 'slc.publications.interfaces.IPublicationEnhanced',
                 path = navigation_root_path,
                 sort_on = 'effective',
                 sort_order = 'reverse')


        st = self.request.get('SearchableText' '')
        if st:
            query.update({'SearchableText': st})

        effective_year = self.request.get('effective_year', '')
        effective_month = self.request.get('effective_month', '')
        effective_day = self.request.get('effective_day', '')
        effective_mode = self.request.get('effective_mode', '')
        edr = self.request.get('effective_days_range', 0)


        if effective_year and effective_month:
            if not effective_day:
                effective_day = 1
            searchdate = DateTime('%d/%d/%d' % (effective_year, effective_month, effective_day))
            if effective_mode=='before':
                query.update(dict(effective=dict(query=searchdate, range='max')))
            elif effective_mode=='after':
                query.update(dict(effective=dict(query=searchdate, range='min')))
            elif effective_mode=='range':
                query.update(dict(effective=dict(query=(searchdate-edr, searchdate+edr), range='min:max')))


        return query



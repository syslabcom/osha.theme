from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
import Acquisition
from zope.component import getMultiAdapter
from DateTime import DateTime
from zope.i18n import translate
import json

from slc.publications.browser.publications import PublicationsView, MAX_RESULTS


class PublicationsSearchView(BrowserView):
    """View for displaying the publications overview page at /xx/publications
    """

    def __call__(self):
        self.request.set('disable_border', True)
        return self.index()

    def getName(self):
        return self.__name__

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
            if keywords and keywords != [""]:
                keywords = keywords[0]
            url = "%s/publications-overview?Subject:list=%s"\
                  % (solution, keywords)
        return url

class PublicationsListView(BrowserView):
    """ View for displaying publications by subfolder. Replaces index_html
    """

    def getContents(self):
        """ CMFCore's ContentFilter class (from PortalFolder.py ignores review_state as a
        parameter in the filter. Therefore we need to define our own query and cannot use
        listFolderContents."""
        pc = getToolByName(self.context, 'portal_catalog')
        path = '/'.join(self.context.getPhysicalPath())
        query = {'portal_type': 'Folder', 'review_state': ['published'],
                'path': {'query': path, 'depth': 1}, 'sort_on': 'getObjPositionInParent' }
        return pc(query)

    def __call__(self):
        self.request.set('disable_border', True)
        return self.index()

    def getName(self):
        return self.__name__


class QuestionsInParliamentSearchView(BrowserView):
    """ View for displaying the publications search page for Questions In Parliament on BeSWIC.be
    """

    def __call__(self):
        self.request.set('disable_border', True)
        return self.index()

    def getName(self):
        return self.__name__


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

class LanguageFallbackView(PublicationsView):
    """Publications view with language fallback"""

    def get_publications(self):
        form = self.request.form
        typelist = form.get("typelist", "")
        search_path = self.path
        if typelist:
            search_path += "/" + typelist
        keywords = form.get("keywords")
        query = {
            'object_provides':
                'slc.publications.interfaces.IPublicationEnhanced',
            'review_state': 'published',
            'SearchableText': form.get("SearchableText", ''),
            'path': search_path,
            'sort_on': 'effective',
            'sort_order': 'descending'
            }
        if keywords:
            query['Subject'] = keywords

        search_view = self.context.restrictedTraverse('@@language-fallback-search')
        brains = search_view.search(query)

        show_all = form.get("show-all", False)
        results = show_all and brains or brains[:MAX_RESULTS]
        if len(brains) > MAX_RESULTS and show_all == False:
            self.has_more_results = True

        publications = []

        for result in results:
            path = result.getPath()
            title = result.Title.replace("'", "&#39;")

            # Searches without SearchableText are sent to the normal
            # portal_catalog and the Title returned is a string
            if not isinstance(title, unicode):
                title.decode("utf-8")

            pub_type = self.get_publication_type(path)
            type_info = self.publication_types.get(pub_type)
            type_title = type_info and type_info['title'] or u''

            portal_languages = getToolByName(
                self.context, 'portal_languages')
            preflang = portal_languages.getPreferredLanguage()

            # Need to translate the type_name here for the JSON version
            translated_type_title = translate(
                type_title,
                domain="slc.publications",
                target_language=preflang,
                )
            publications.append({
                "title": title,
                "year": result.effective.year(),
                "size": result.getObjSize,
                "path": path + "/view",
                "type": pub_type,
                "type_title": translated_type_title,
            })
        return publications


class PublicationsJSONView(LanguageFallbackView):
    """Return search results in JSON"""

    def __call__(self):
        return json.dumps(self.get_publications())

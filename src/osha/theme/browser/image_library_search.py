from Acquisition import aq_inner, aq_parent
from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from osha.theme.browser.dbfilter import DBFilterView


class ImageLibrarySearchView(DBFilterView):
    """View for the Image Library Search.
    
    This makes a specialised search form which is used to retrieve images from the 
    Digital Assets library.
    It searches only for images and files in the current section and
    shows the results as a gallery view.
    """

    template = ViewPageTemplateFile('templates/image_library_search.pt')
    template.id = "image-library-search"

    portal_types_map = {
            "useful-links":"OSH_Link",
            "risk-assessment-tools":"RALink",
            "case-studies":"CaseStudy",
            "providers":"Provider",
            "faqs":"FAQs",
            "publications": "Publication"
            }

    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()

    def get_keyword(self):
        """ Return the first value from keywords/request or an empty string
        """
        keywords = self.request.get("keywords", "")
        keyword = ""
        if keywords:
            keyword = keywords[0]
        return keyword

    def buildQuery(self):
        """ Build the query based on the request.
        Overriding this method from DBFilter because it treats an
        empty keywords:list as a value causing nothing to be returned
        """
        context = aq_inner(self.context)
        query = In('portal_type', ['Image', 'File'])

        keywords = self.request.get('keywords', [])
        if keywords:
            if keywords !=  ['']:
                query = query & In('Subject', keywords)

        nace = list(self.request.get('nace', ''))
        if '' in nace:
            nace.remove('')
        if nace:
            query = query & In('nace', nace)
            #query.update({'nace':nace})

        multilingual_thesaurus = list(
            self.request.get('multilingual_thesaurus', '')
            )
        if '' in multilingual_thesaurus:
            multilingual_thesaurus.remove('')
        if multilingual_thesaurus:
            query = query & In('multilingual_thesaurus', multilingual_thesaurus)
            #query.update({'multilingual_thesaurus':multilingual_thesaurus})

        SearchableText = self.request.get('SearchableText', '')
        if SearchableText != '':
            query = query & Generic(
                'SearchableText',
                {'query': SearchableText, 'ranking_maxhits': 1000 }
                )
            #query.update({'SearchableText': {'query': SearchableText, 'ranking_maxhits': 10000 }})

        return query

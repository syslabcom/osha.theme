import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic



class DBFilterView(BrowserView):
    """View for displaying the sep content filter page at /en/good_practice/topics/xx
    It creates a search query based on the input from the template and returns the results.
    This is just another advanced search form.


    """
    template = ViewPageTemplateFile('templates/dbfilter.pt')
    template.id = "db_filter"

    def __call__(self):
        #self.request.set('disable_border', True)

        return self.template()

    def search_types(self):
        """ returns a list of translated search types to select from """
        context = Acquisition.aq_inner(self.context)

        local_portal_types = context.getProperty('search_portal_types', [])
        search_portal_types = self.request.get('search_portal_types', local_portal_types)
        # if all are turned off, turn them all on. Searching for nothing makes no sense.
        if not search_portal_types:
            search_portal_types = ['OSH_Link', 'RALink', 'CaseStudy', 'Provider', 'Publication']
        TYPES = [
            ('OSH Link', 'OSH_Link', 'OSH_Link' in search_portal_types) ,
            ('Risk Assessment Link', 'RALink', 'RALink' in search_portal_types) ,
            ('Case Study', 'CaseStudy', 'CaseStudy' in search_portal_types) ,
            ('Provider', 'Provider', 'Provider' in search_portal_types) ,
            ('Publication', 'Publication', 'Publication' in search_portal_types)
                ]

        return TYPES

    def search_portal_types(self):
        """ compute the list of query params to search for portal_types"""
        context = Acquisition.aq_inner(self.context)
        #local_portal_types = context.getProperty('search_portal_types', []);
        # we need to use the output of search_types() as default, not the
        # local Property search_portal_types
        search_types = [x[1] for x in self.search_types()]
        search_portal_types = list(self.request.get('search_portal_types', search_types))

        query = None
        if 'Publication' in search_portal_types:
            query = ( Eq('portal_type', 'File') & Eq('object_provides', 'slc.publications.interfaces.IPublicationEnhanced') )
            search_portal_types.remove('Publication')
            query = Or(query, In('portal_type', search_portal_types))
        else:
            query = In('portal_type', search_portal_types)


        return query

    def buildQuery(self):
        """ Build the query based on the request """
        context = Acquisition.aq_inner(self.context)

        query = self.search_portal_types()

        #query = { 'sort_on': 'effective',
        #          'sort_order':'reverse',
        #          'Language': ''}

        local_keyword = context.getProperty('keyword', '')
        keywords = self.request.get('keywords', local_keyword)
        if keywords:
            query = query & In('Subject', keywords)
            #query.update({'Subject':keywords})

        nace = list(self.request.get('nace', ''))
        if '' in nace:
            nace.remove('')
        if nace:
            query = query & In('nace', nace)
            #query.update({'nace':nace})

        multilingual_thesaurus = list(self.request.get('multilingual_thesaurus', ''))
        if '' in multilingual_thesaurus:
            multilingual_thesaurus.remove('')
        if multilingual_thesaurus:
            query = query & In('multilingual_thesaurus', multilingual_thesaurus)
            #query.update({'multilingual_thesaurus':multilingual_thesaurus})

        getRemoteLanguage = self.request.get('getRemoteLanguage', '')
        if getRemoteLanguage:
            query = query & In('getRemoteLanguage', getRemoteLanguage)
            #query.update({'getRemoteLanguage':getRemoteLanguage})

        subcategory = self.request.get('subcategory', '')
        if subcategory:
            query = query & In('subcategory', subcategory)
            #query.update({'subcategory':subcategory})

        country = self.request.get('country', '')
        if country:
            query = query & In('country', country)
            #query.update({'country':country})

        SearchableText = self.request.get('SearchableText', '')
        if SearchableText != '':
            query = query & Generic('SearchableText', {'query': SearchableText, 'ranking_maxhits': 10000 })
            #query.update({'SearchableText': {'query': SearchableText, 'ranking_maxhits': 10000 }})


        return query


    def search(self):
        context = Acquisition.aq_inner(self.context)
        query = self.buildQuery()
        portal_catalog = getToolByName(context, 'portal_catalog')
        if hasattr(portal_catalog, 'getZCatalog'):
            portal_catalog = portal_catalog.getZCatalog()

        return portal_catalog.evalAdvancedQuery(query, (('effective','desc'),))


class ProviderDBFilterView(DBFilterView):
    """View for displaying the GP content filter page for Providers
    """
    template = ViewPageTemplateFile('templates/index_provider.pt')
    template.id = "index_provider"

    def search_types(self):
        """ returns a list of translated search types to select from """
        return [ ('Provider', 'Provider', True) ]


class OSHLinkDBFilterView(DBFilterView):
    """View for displaying the GP content filter page for OSHLinks
    """
    template = ViewPageTemplateFile('templates/index_oshlink.pt')
    template.id = "index_oshlink"

    def search_types(self):
        """ returns a list of translated search types to select from """
        return [('OSH Link', 'OSH_Link', True)]


class RALinkDBFilterView(DBFilterView):
    """View for displaying the GP content filter page for RALinks
    """
    template = ViewPageTemplateFile('templates/index_ralink.pt')
    template.id = "index_ralink"

    def search_types(self):
        """ returns a list of translated search types to select from """
        return [('Risk Assessment Link', 'RALink', True)]

class CaseStudyDBFilterView(DBFilterView):
    """View for displaying the GP content filter page for CaseStudies
    """
    template = ViewPageTemplateFile('templates/index_casestudy.pt')
    template.id = "index_casestudy"

    def search_types(self):
        """ returns a list of translated search types to select from """
        return [('Case Study', 'CaseStudy', True)]

class DirectiveDBFilterView(DBFilterView):
    """View for displaying the GP content filter page for Directives
    """
    template = ViewPageTemplateFile('templates/index_directive.pt')
    template.id = "index_directive"

    def search_types(self):
        """ returns a list of translated search types to select from """
        return [('Directives', 'Directive', True)]

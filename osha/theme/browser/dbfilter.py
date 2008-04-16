import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class DBFilterView(BrowserView):
    """View for displaying the sep content filter page at /en/good_practice/topics/xx
    """
    template = ViewPageTemplateFile('templates/dbfilter.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)

        return self.template() 

    def search_types(self):
        """ returns a list of translated search types to select from """
        context = Acquisition.aq_inner(self.context)
        
        local_portal_types = context.getProperty('search_portal_types', [])
        search_portal_types = self.request.get('search_portal_types', local_portal_types)
        
        TYPES = [ 
            ('OSH Link', 'OSH_Link', 'OSH_Link' in search_portal_types) ,
            ('Risk Assessment Link', 'RiskAssessmentLink', 'RiskAssessmentLink' in search_portal_types) ,
            ('Case Study', 'CaseStudy', 'CaseStudy' in search_portal_types) ,
            ('Provider', 'Provider', 'Provider' in search_portal_types) ,
            ('Publication', 'Publication', 'Publication' in search_portal_types)
                ]
                
        
        return TYPES

    def search_portal_types(self):
        """ compute the list of query params to search for portal_types"""
        context = Acquisition.aq_inner(self.context)
        local_portal_types = context.getProperty('search_portal_types', []);
        search_portal_types = list(self.request.get('search_portal_types', local_portal_types))

        query = {}
        if 'Publication' in search_portal_types:
            search_portal_types.remove('Publication')
            search_portal_types.append('File')
            query.update({'object_implements': 'slc.publications.interfaces.IPublicationEnhanced'})
            
        query.update({'portal_type': search_portal_types})
        return query
        
    def buildQuery(self):
        """ Build the query based on the request """
        context = Acquisition.aq_inner(self.context)
        query = { 'sort_on': 'effective',
                  'sort_order':'reverse',
                  'Language': ''}

        local_keyword = context.getProperty('keyword', '')
        keywords = self.request.get('keywords', local_keyword)
        if keywords:
            query.update({'Subject':keywords})

        nace = list(self.request.get('nace', ''))
        if '' in nace:
            nace.remove('')
        if nace:
            query.update({'nace':nace})

        multilingual_thesaurus = list(self.request.get('multilingual_thesaurus', ''))
        if '' in multilingual_thesaurus:
            multilingual_thesaurus.remove('')
        if multilingual_thesaurus:
            query.update({'multilingual_thesaurus':multilingual_thesaurus})

        getRemoteLanguage = self.request.get('getRemoteLanguage', '')
        if getRemoteLanguage:
            query.update({'getRemoteLanguage':getRemoteLanguage})

        subcategory = self.request.get('subcategory', '')        
        if subcategory:
            query.update({'subcategory':subcategory})

        getCountry = self.request.get('getCountry', '')
        if getCountry:
            query.update({'getCountry':getCountry})

        SearchableText = self.request.get('SearchableText', '')
        if SearchableText != '':
            query.update({'SearchableText':SearchableText})

        search_portal_types = self.search_portal_types()
        query.update(search_portal_types)

        return query
        
        

        
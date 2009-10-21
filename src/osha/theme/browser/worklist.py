import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic

from osha.theme.browser.dbfilter import DBFilterView

class WorklistView(DBFilterView):
    """View for displaying the worklist (filter plus result list)
    """
    template = ViewPageTemplateFile('templates/worklist.pt')
    template.id = "worklist"

    def __call__(self):
        self.request.set('disable_border', True)

        return self.template() 

    def search_types(self):
        """ returns a list of translated search types to select from 
        This method is overwritten from dbfilter to provide a default list of types, so that all 
        are selected initially"""
        context = Acquisition.aq_inner(self.context)
        
        default = ['OSH_Link', 'RALink', 'CaseStudy', 'Provider', 'Publication', 'Directive', 'Modification','Amendment','Note','Proposal']
        local_portal_types = context.getProperty('search_portal_types', default)
        search_portal_types = self.request.get('search_portal_types', local_portal_types)
        if not search_portal_types:
            search_portal_types = default

        TYPES = [ 
            ('OSH Link', 'OSH_Link', 'OSH_Link' in search_portal_types) ,
            ('Risk Assessment Link', 'RALink', 'RALink' in search_portal_types) ,
            ('Case Study', 'CaseStudy', 'CaseStudy' in search_portal_types) ,
            ('Provider', 'Provider', 'Provider' in search_portal_types) ,
            ('Publication', 'Publication', 'Publication' in search_portal_types) ,
            ('Legislation Directive', 'Directive', 'Directive' in search_portal_types),
            ('Legislation Modification', 'Modification', 'Modification' in search_portal_types),
            ('Legislation Amendment', 'Amendment', 'Amendment' in search_portal_types),
            ('Legislation Note', 'Note', 'Note' in search_portal_types),
            ('Legislation Proposal', 'Proposal', 'Proposal' in search_portal_types)
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

        country = self.request.get('country', '')
        if country:
            query = query & In('country', country)    
            #query.update({'country':country})

        SearchableText = self.request.get('SearchableText', '')
        if SearchableText != '':
            query = query & Generic('SearchableText', {'query': SearchableText, 'ranking_maxhits': 10000 })
            #query.update({'SearchableText': {'query': SearchableText, 'ranking_maxhits': 10000 }})

        
        
        Creator = self.request.get('Creator', '')
        if Creator:
            query = query & Eq('Creator', Creator)
            #query.update(dict(Creator=Creator))

        subcategory = list(self.request.get('subcategory', ''))
        if '' in subcategory:
            subcategory.remove('')
        if subcategory:
            query = query & In('subcategory', subcategory)    
            #query.update({'subcategory':subcategory})

        getRemoteUrl = self.request.get('getRemoteUrl', '')
        if getRemoteUrl:
            query = query & Eq('getRemoteUrl', getRemoteUrl)    
            #query.update(dict(getRemoteUrl=getRemoteUrl))

        review_state = self.request.get('review_state', ['private', 'published', 'to_amend', 'pending', 'checked'])
        if review_state:
            query = query & In('review_state', review_state)    

        lang = getToolByName(self.context, 'portal_languages').getPreferredLanguage() 
        query = query & In('Language', [lang, ''])
        return query
        
        

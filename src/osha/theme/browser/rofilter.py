import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class ROFilterView(BrowserView):
    """View for displaying the ro content filter page 
    """
    template = ViewPageTemplateFile('templates/rofilter.pt')

    def __call__(self):
        self.request.set('disable_border', True)

        return self.template() 

    def search_portal_types(self):
        """ compute the list of query params to search for portal_types"""
        context = Acquisition.aq_inner(self.context)    
        query = {}       
        query.update({'portal_type': 'RichDocument'})
        return query
        
    def buildQuery(self):
        """ Build the query based on the request """
        context = Acquisition.aq_inner(self.context)
        query = { 'sort_on': 'effective',
                  'sort_order':'reverse',
                  'Language': ''}

                  

        ero_topic = self.request.get('ero_topic', None)
        if ero_topic:
            query.update({'ero_topic':ero_topic})

        ero_target_group = self.request.get('ero_target_group', None)
        if ero_target_group:
            query.update({'ero_target_group':ero_target_group})

        country = self.request.get('country', '')
        if country:
            query.update({'country':country})

        SearchableText = self.request.get('SearchableText', '')
        if SearchableText != '':
            query.update({'SearchableText':{'query':SearchableText, 'ranking_maxhits': 10000}})

        search_portal_types = self.search_portal_types()
        query.update(search_portal_types)

        return query
        
        

    def results(self):
        """ build the query and do the search """
        context = Acquisition.aq_inner(self.context)
        portal_catalog = getToolByName(context, 'portal_catalog')
        query = self.buildQuery()
        results = portal_catalog(query)
        return results
                      
import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

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
        
        default = ['OSH_Link', 'RALink', 'CaseStudy', 'Provider', 'Publication']
        local_portal_types = context.getProperty('search_portal_types', default)
        search_portal_types = self.request.get('search_portal_types', local_portal_types)
        
        TYPES = [ 
            ('OSH Link', 'OSH_Link', 'OSH_Link' in search_portal_types) ,
            ('Risk Assessment Link', 'RALink', 'RALink' in search_portal_types) ,
            ('Case Study', 'CaseStudy', 'CaseStudy' in search_portal_types) ,
            ('Provider', 'Provider', 'Provider' in search_portal_types) ,
            ('Publication', 'Publication', 'Publication' in search_portal_types)
                ]
        return TYPES

    def buildQuery(self):
        """ Build the query based on the request """
        context = Acquisition.aq_inner(self.context)
        query = super(WorklistView, self).buildQuery()

        Creator = self.request.get('Creator', '')
        if Creator:
            query.update(dict(Creator=Creator))

        country = self.request.get('country', '')
        if country:
            query.update(dict(country=country))

        # remove wrongly formatted subcategory from query
        if query.has_key('subcategory'):
            del query['subcategory']
        subcategory = list(self.request.get('subcategory', ''))
        if '' in subcategory:
            subcategory.remove('')
        if subcategory:
            query.update({'subcategory':subcategory})

        getRemoteUrl = self.request.get('getRemoteUrl', '')
        if getRemoteUrl:
            query.update(dict(getRemoteUrl=getRemoteUrl))

        review_state = self.request.get('review_state', '')
        if review_state:
            query.update(dict(review_state=review_state))

        return query
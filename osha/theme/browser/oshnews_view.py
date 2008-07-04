import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from osha.theme import OSHAMessageFactory as _
from zope.component import getMultiAdapter
from Products.AdvancedQuery import Or, Eq, And, In
from plone.memoize.instance import memoize
from Products.CMFPlone.PloneBatch import Batch

class OSHNewsView(BrowserView):
    """View for displaying news outside the current context within the context
    """
    template = ViewPageTemplateFile('templates/oshnews_view.pt')
    template.id = "oshnews-view"
    
    def __call__(self):
        
        return self.template() 
        
    def Title(self):
        return _(u"heading_newsboard_latest_news")
    
    @memoize
    def queryCatalog(self, b_size=20):

        context = Acquisition.aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        if hasattr(catalog, 'getZCatalog'):
            catalog = catalog.getZCatalog()
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()

        oshaview = getMultiAdapter((self.context, self.request), name=u'oshaview')
        mySEP = oshaview.getCurrentSingleEntryPoint()
        kw = ''
        if mySEP is not None:
            kw = mySEP.getProperty('keyword', '')
            
        queryA = Eq('portal_type', 'News Item')
        queryB = Eq('isNews', True)
        queryBoth = In('review_state', 'published') & Eq('path', navigation_root_path) 
        if kw !='':
            queryBoth = queryBoth & In('Subject', kw)
        query = And(Or(queryA, queryB), queryBoth)
        results = catalog.evalAdvancedQuery(query, (('Date', 'desc'),) ) 
        
        
        b_start = self.request.get('b_start', 0)
        batch = Batch(results, b_size, int(b_start), orphan=0)

        return batch
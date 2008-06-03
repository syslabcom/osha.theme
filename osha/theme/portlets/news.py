from plone.app.portlets.portlets import news
from Products.AdvancedQuery import Or, Eq, And, In
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

class Renderer(news.Renderer):
    """Dynamically override standard header for news portlet"""
    
    _template = ViewPageTemplateFile('news.pt')
        
    # Add respect to INavigationRoot
    # Add support for isNews flag
    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()

        oshaview = getMultiAdapter((self.context, self.request), name=u'oshaview')
        mySEP = oshaview.getCurrentSingleEntryPoint()
        kw = ''
        if mySEP is not None:
            kw = mySEP.getProperty('keyword', '')
            
        limit = self.data.count
        state = self.data.state
        
        queryA = Eq('portal_type', 'News Item')
        queryB = Eq('isNews', True)
        queryBoth = In('review_state', state) & Eq('path', navigation_root_path) 
        if kw !='':
            queryBoth = queryBoth & In('Subject', kw)
        query = And(Or(queryA, queryB), queryBoth)
        return catalog.evalAdvancedQuery(query, (('Date', 'desc'),) )[:limit]

    def all_news_link(self):
        context = aq_inner(self.context)
        if not context.isPrincipiaFolderish:
            context = aq_parent(context)
        
        return '%s/oshnews-view' % context.absolute_url()

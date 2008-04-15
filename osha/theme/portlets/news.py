from plone.app.portlets.portlets import news
from Products.AdvancedQuery import Or, Eq, And, In
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

class Renderer(news.Renderer):
    """Dynamically override standard header for news portlet"""
    
    _template = ViewPageTemplateFile('news.pt')

    @property
    def available(self):
        return len(self._data())
        
    # Add respect to INavigationRoot
    # Add support for isNews flag
    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        limit = self.data.count
        state = self.data.state
        
        queryA = Eq('portal_type', 'News Item')
        queryB = Eq('isNews', True)
        queryBoth = In('review_state', state) & Eq('path', navigation_root_path) 
        query = And(Or(queryA, queryB), queryBoth)
        res = catalog.evalAdvancedQuery(query, (('Date', 'desc'),) )[:limit]

        return res

from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
        

class SitemapQueryBuilder(NavtreeQueryBuilder):
    """Build a folder tree query suitable for a sitemap
    """

    def __init__(self, context):
        NavtreeQueryBuilder.__init__(self, context)
        portal_url = getToolByName(context, 'portal_url')
        
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        sitemapDepth = navtree_properties.getProperty('sitemapDepth', 2)
        self.query['path'] = {'query' : navigation_root_path,
                              'depth' : sitemapDepth}

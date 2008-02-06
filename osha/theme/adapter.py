from StringIO import StringIO

from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter, queryUtility

from plone.memoize import ram
from plone.memoize.instance import memoize
from plone.memoize.compress import xhtml_compress

from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.portlets.portlets.navigation import INavigationPortlet, getRootPath

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from plone.app.layout.navigation.root import getNavigationRoot
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy

# Special Query Builder for the Root object to build a query which takes the 
# language trees into account and shows the 2nd level navi below /en, /de, etc.

class QueryBuilder(object):
    """Build a navtree query based on the settings in navtree_properties
    and those set on the portlet.
    """
    implements(INavigationQueryBuilder)
    adapts(ISiteRoot, INavigationPortlet)

    def __init__(self, context, portlet):
        self.context = context
        self.portlet = portlet
        print "I am in the site root and I am a navi query builder"
        
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        
        portal_url = getToolByName(context, 'portal_url')
        
        portal_languages = getToolByName(context, 'portal_languages')
        
        # Acquire a custom nav query if available
        customQuery = getattr(context, 'getCustomNavQuery', None)
        if customQuery is not None and utils.safe_callable(customQuery):
            query = customQuery()
        else:
            query = {}
        #import pdb;pdb.set_trace()
        # Construct the path query
        preferred_path = "/%s" % portal_languages.getPreferredLanguage()
        
        #rootPath = getNavigationRoot(context, relativeRoot=portlet.root)
        rootPath = getNavigationRoot(context, relativeRoot=preferred_path)
        currentPath = '/'.join(context.getPhysicalPath())

        # If we are above the navigation root, a navtree query would return
        # nothing (since we explicitly start from the root always). Hence,
        # use a regular depth-1 query in this case.

#        if not currentPath.startswith(rootPath):
#            query['path'] = {'query' : rootPath, 'depth' : 2}
#        else:
#            query['path'] = {'query' : currentPath, 'navtree' : 1}
        query['path'] = {'query' : rootPath, 'navtree' : 1, 'navtree_start': 2}

        topLevel = portlet.topLevel or navtree_properties.getProperty('topLevel', 0)
        topLevel = 0
#        if topLevel and topLevel > 0:
#             query['path']['navtree_start'] = topLevel + 1

        # XXX: It'd make sense to use 'depth' for bottomLevel, but it doesn't
        # seem to work with EPI.

        # Only list the applicable types
        query['portal_type'] = utils.typesToList(context)

        # Apply the desired sort
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        # Filter on workflow states, if enabled
        if navtree_properties.getProperty('enable_wf_state_filtering', False):
            query['review_state'] = navtree_properties.getProperty('wf_states_to_show', ())

        self.query = query
        print query
        
    def __call__(self):
        return self.query
       
       
       
       
       
class NavtreeStrategy(SitemapNavtreeStrategy):
    """The navtree strategy used for the default navigation portlet
    """
    implements(INavtreeStrategy)
    adapts(ISiteRoot, INavigationPortlet)

    def __init__(self, context, portlet):
        SitemapNavtreeStrategy.__init__(self, context, portlet)
        portal_properties = getToolByName(context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        portal_languages = getToolByName(context, 'portal_languages')
        
        # XXX: We can't do this with a 'depth' query to EPI...
        self.bottomLevel = portlet.bottomLevel or navtree_properties.getProperty('bottomLevel', 0)

        currentFolderOnly = portlet.currentFolderOnly or navtree_properties.getProperty('currentFolderOnlyInNavtree', False)
        topLevel = portlet.topLevel or navtree_properties.getProperty('topLevel', 0)
        #self.rootPath = getRootPath(context, currentFolderOnly, topLevel, portlet.root)
        self.rootPath = "%s/%s" % (getRootPath(context, currentFolderOnly, topLevel, portlet.root), portal_languages.getPreferredLanguage())
        self.showAllParents = False


    def subtreeFilter(self, node):
        sitemapDecision = SitemapNavtreeStrategy.subtreeFilter(self, node)
        if sitemapDecision == False:
            return False
        depth = node.get('depth', 0)
        if depth > 0 and self.bottomLevel > 0 and depth >= self.bottomLevel:
            return False
        else:
            return True        
 
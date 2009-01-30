from StringIO import StringIO

from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter, queryUtility

from plone.memoize import ram
from plone.memoize.instance import memoize
from plone.memoize.compress import xhtml_compress

from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.root import getNavigationRoot
from plone.app.portlets.portlets.navigation import INavigationPortlet, getRootPath

from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from Products.CMFPlone.browser.navtree import SitemapNavtreeStrategy

# Special Query Builder for the Root object to build a query which takes the 
# language trees into account and shows the 2nd level navi below /en, /de, etc.

class ITopLevelNavigation(Interface):
    """ Marker Interface to enable the special linguaplone top level navigation which 
        shows only the folders within the current language top folder"""

class QueryBuilder(object):
    """Build a navtree query based on the settings in navtree_properties
    and those set on the portlet.
    """
    implements(INavigationQueryBuilder)
    adapts(ITopLevelNavigation, INavigationPortlet)

    def __init__(self, context, portlet):
        self.context = context
        self.portlet = portlet
        
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
        
        rootPathX = getNavigationRoot(context, relativeRoot=portlet.root)
        rootPathY = getNavigationRoot(context, relativeRoot=preferred_path)
        
        rootPath = portal_url.getPortalPath()+preferred_path

        print "X: portlet.root based. rootPath: %s, portlet.root: %s" %(rootPathX, portlet.root)
        print "Y: preferred_path based. rootPath: %s, preferred_path: %s" %(rootPathY, preferred_path)
        print "Current: rootPath+preferred_path: %s %s" %(rootPath, preferred_path)

        currentPath = '/'.join(context.getPhysicalPath())

        # If we are above the navigation root, a navtree query would return
        # nothing (since we explicitly start from the root always). Hence,
        # use a regular depth-1 query in this case.

        query['path'] = {'query' : rootPath, 'navtree' : 1, 'navtree_start': 1}

        topLevel = portlet.topLevel or navtree_properties.getProperty('topLevel', 0)
        topLevel = 0

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
        
    def __call__(self):
        return self.query
       
       
       
       
       
class NavtreeStrategy(SitemapNavtreeStrategy):
    """The navtree strategy used for the default navigation portlet
    """
    implements(INavtreeStrategy)
    adapts(ITopLevelNavigation, INavigationPortlet)

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
        #self.rootPath = "%s/%s" % ( getRootPath(context, currentFolderOnly, topLevel, portlet.root), portal_languages.getPreferredLanguage())
        portal_url = getToolByName(context, 'portal_url')
        portal_root = portal_url.getPortalPath()
        
        self.rootPath = "%s/%s" % ( portal_root, portal_languages.getPreferredLanguage())
        if "//" in self.rootPath:
            self.rootPath = self.rootPath.replace("//","/")
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
 

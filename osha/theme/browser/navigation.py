from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.Five import BrowserView
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.interfaces import ISiteMap

from navtree import SitemapQueryBuilder

from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree


class CatalogSiteMap(BrowserView):
    implements(ISiteMap)

    def siteMap(self):
        context = aq_inner(self.context)

        queryBuilder = SitemapQueryBuilder(context)
        query = queryBuilder()

        strategy = getMultiAdapter((context, self), INavtreeStrategy)

        return buildFolderTree(context, obj=context, query=query, strategy=strategy)

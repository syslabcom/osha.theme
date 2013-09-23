from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getMultiAdapter
from Products.Five import BrowserView
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

        # Fixes #8569: "Sitemap not working":
        if 'is_default_page' in strategy.supplimentQuery:
            del strategy.supplimentQuery['is_default_page']

        return buildFolderTree(
            context, obj=context, query=query, strategy=strategy)

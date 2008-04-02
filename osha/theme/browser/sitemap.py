from plone.app.layout.sitemap.sitemap import SiteMapView as BaseView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from types import *

class SiteMapView(BaseView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """

    template = ViewPageTemplateFile('templates/sitemap.xml')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.filename = 'sitemap.xml.gz'

    def objects(self):
        """Returns the data to create the sitemap."""
        catalog = getToolByName(self.context, 'portal_catalog')
        for item in catalog.searchResults({'Language': 'all'}):
            lastmod = item.modified
            try:
                lastmod = lastmod.ISO8601()
            except:
                lastmod = '2008-01-01T1:00:00+00:00'
                
            changefreq = item.get('changefreq', "monthly")
            priority = item.get('priority', 0.5)
            
            yield {
                'loc': item.getURL(),
                'lastmod': lastmod,
                'changefreq': changefreq, # hourly/daily/weekly/monthly/yearly/never
                'priority': priority, # 0.0 to 1.0
            }


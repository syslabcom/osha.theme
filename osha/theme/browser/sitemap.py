from plone.app.layout.sitemap.sitemap import SiteMapView as BaseView
from Products.CMFCore.utils import getToolByName
from zope.app.component.hooks import getSite
from zope.publisher.interfaces import NotFound
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime import DateTime
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
        self.urlmap = self.parseUrlFile()

    def __call__(self):
        """Checks if the sitemap feature is enable and returns it."""
        sp = getToolByName(self.context, 'portal_properties').site_properties
        if not sp.enable_sitemap:
            raise NotFound(self.context, self.filename, self.request)

        self.request.response.setHeader('Content-Type',
                                        'application/octet-stream')
        data = self.generate()                                
        self.persistFile(data)
        return data

    def persistFile(self, data):
        """ write the map into a file object to avoid google download timeouts """
        site = getSite()
        id = 'sitemap_p.xml.gz'
        if id not in site.objectIds():
            site.manage_addFile(id)
        F = getattr(site, id)
        F.update_data(data)
        F.content_type='application/octet-stream'
        
    def parseUrlFile(self):
        """ parses a simple file with format url,changefreq,priority """
        urlfile = getattr(self.context, 'sitemap_urlfile', None)
        if urlfile is None:
            return {}
        urldata = str(urlfile.data)
        urlmap = {}
        for line in urldata.split("\n"):
            elems = line.split(",")
            if len(elems)>2:
                urlmap[elems[0].strip()] = (elems[1].strip(), elems[2].strip())
                
        return urlmap

    def objects(self):
        """Returns the data to create the sitemap."""
        catalog = getToolByName(self.context, 'portal_catalog')
        portal_url = getToolByName(self.context, 'portal_url')
        
        # the main url does not turn up as a catalog result so we do it manually
        yield {
            'loc': portal_url(),
            'lastmod': DateTime().ISO8601(),
            'changefreq': 'always', 
            'priority': 1
        }        
        
        for item in catalog.searchResults({'Language': 'all'}):
            # We only want to link them in the search form results
            if item.portal_type in ['OSH_Link', 'RALink', 'CaseStudy', 'Provider']:
                continue
            try:
                lastmod = item.modified.ISO8601()
            except:
                lastmod = '2008-01-01T1:00:00+00:00'
                
            loc = item.getURL()

            changefreq = item.get('changefreq', "monthly")
            priority = item.get('priority', 0.3)           

            if item.portal_type in ['Event', 'News Item']:
                changefreq = "never"
                if item.effective<(DateTime()-30):
                    priority = 0.3
                else:
                    priority = 0.9

            # manually set urlmap overrides
            if self.urlmap.has_key(loc):    
                changefreq, priority = self.urlmap[loc]
            
            yield {
                'loc': loc,
                'lastmod': lastmod,
                'changefreq': changefreq, # hourly/daily/weekly/monthly/yearly/never
                'priority': priority, # 0.0 to 1.0
            }


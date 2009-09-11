import Acquisition, time
from plone.memoize import ram
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

class SiteUpdateView(BrowserView):
    """View for displaying the latest update on the site
    """
    template = ViewPageTemplateFile('templates/site_update.pt')
    template.id = 'site_update'
    
    def __call__(self):
        self.request.set('disable_border', True)
        context = Acquisition.aq_inner(self.context)        
        
        portal_catalog = getToolByName(context, 'portal_catalog')
        portal_languages = getToolByName(context, 'portal_languages')
        self.lang = portal_languages.getPreferredLanguage()
        self.items = self._searchCatalog()
        return self.template() 
        
    def results(self):
        context = Acquisition.aq_inner(self.context)        
        toLocalizedTime = context.restrictedTraverse('@@plone').toLocalizedTime
        all = []
        currday = None
        for i in self.items:
            modified = i.get('modified')
            day = toLocalizedTime(modified)
            if day != currday:            
                all.append((day, i))
                currday = day
            else:
                all.append((None, i))
                
        return all

    def _searchCatalog_cachekey(method, self):
        return ("site_update", self.lang)    
        
    @ram.cache(_searchCatalog_cachekey)
    def _searchCatalog(self):
        """ search the catalog for recent items  
            this is to be cached 
        """
        start = time.time()

        context = Acquisition.aq_inner(self.context)        
        portal_catalog = getToolByName(context, 'portal_catalog')
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        
        query = {'limit':100,
                 'review_state': 'published',
                 'portal_type': ['Document', 'RichDocument', 'News Item', 'Event'],
                 'sort_on': 'modified',
                 'sort_order': 'reverse',
                 'path': navigation_root_path
                }
        results = portal_catalog(query)[:100]                
        stop = time.time()
        print "Catalog time is %s" % (stop-start)
        # The brain objects fetch the values potentially lazy only if needed. 
        # This may be bad for caching and seems to result in the hard to debug 
        # ConnectionStateError: Shouldn't load state for 0x3768d0 when the connection is closed error. 
        # I therefore copy the results over into a static datastructure.
        sres = []
        schema = portal_catalog.schema()
        for result in results:
            staticbrain = {}
            for key in schema:
                staticbrain[key] = result[key]
            staticbrain['getURL'] = result.getURL()
            staticbrain['getPath'] = result.getPath()
            
            sres.append(staticbrain)
            
        return sres
        
             
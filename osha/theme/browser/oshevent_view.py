import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from osha.theme import OSHAMessageFactory as _
from zope.component import getMultiAdapter
from Products.AdvancedQuery import Or, Eq, And, In
from plone.memoize.instance import memoize
from Products.CMFPlone.PloneBatch import Batch
from DateTime import DateTime

class OSHEventView(BrowserView):
    """View for displaying events outside the current context within the context
    """
    template = ViewPageTemplateFile('templates/oshevent_view.pt')
    
    def __call__(self):
        
        return self.template() 
        
    def Title(self):
        return _(u"Events")        
        
    @memoize
    def queryCatalog(self, b_size=10):
        context = Acquisition.aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()

        oshaview = getMultiAdapter((self.context, self.request), name=u'oshaview')
        mySEP = oshaview.getCurrentSingleEntryPoint()
        kw = ''
        if mySEP is not None:
            kw = mySEP.getProperty('keyword', '')


        query = dict(portal_type='Event',
                       review_state='published',
                       path=navigation_root_path,
                       sort_on='start'
                       )
        
        if self.request.get('show', '')=='previous':
            query.update(end={'query': DateTime(),
                              'range': 'max'})
        else:
            query.update(end={'query': DateTime(),
                              'range': 'min'})
                            
        if kw !='':
            query.update(Subject=kw)
        results = catalog(query)
        
        b_start = self.request.get('b_start', 0)
        batch = Batch(results, b_size, int(b_start), orphan=0)
        return batch
        
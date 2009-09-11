from plone.app.portlets.portlets import navigation
import Acquisition
from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.app.portlets.cache import render_cachekey


class Renderer(navigation.Renderer):
    """Dynamically override standard header for risq navtree portlet"""
    
    _template = ViewPageTemplateFile('risqnavigation.pt')
    recurse = ViewPageTemplateFile('risqnavigation_recurse.pt')

    def __init__(self, context, request, view, manager, data):
        navigation.Renderer.__init__(self, context, request, view, manager, data)
        
        self.properties = getToolByName(context, 'portal_properties').navtree_properties
        self.urltool = getToolByName(context, 'portal_url')
        print "in init"
            
    @property
    def available(self):
        return True
            
    @memoize
    def links(self):
        linklist = ['index_html', 'why_risq_it', 'what_can_you_risq', '../competition/video', 'edge_safety']
        context = Acquisition.aq_inner(self.context)      
        portal_url = getToolByName(context, 'portal_url')
        portalpath = "/".join(portal_url.getPortalObject().getPhysicalPath())
        mylist = []    
        P = None
        URL = self.request.URL

        for P in self.request.PARENTS:
            if P.getId()== "risq":
                break
        cnt = 0
        for l in linklist:
            cnt += 1
            ob = P.restrictedTraverse(l, None)
            state = False
            if ob is not None:
                obpath = ob.absolute_url()
                if URL.startswith(obpath):
                    state = True
                mylist.append((ob, state, cnt))
            
        return mylist
from plone.app.portlets.portlets import navigation
import Acquisition
from Products.CMFCore.utils import getToolByName

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Renderer(navigation.Renderer):
    """Dynamically override standard header for risq navtree portlet"""
    
    _template = ViewPageTemplateFile('risqnavigation.pt')
    recurse = ViewPageTemplateFile('risqnavigation_recurse.pt')
    
    @property
    def available(self):
        True
            
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
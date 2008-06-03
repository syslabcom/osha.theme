from plone.app.portlets.portlets import navigation
import Acquisition

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Renderer(navigation.Renderer):
    """Dynamically override standard header for risq navtree portlet"""
    
    _template = ViewPageTemplateFile('risqnavigation.pt')
    recurse = ViewPageTemplateFile('risqnavigation_recurse.pt')
    
    linklist = ['index_html', 'why_risq_it', 'what_can_you_risq', '../competition/video', 'edge_safety']
    
    def links(self):
        context = Acquisition.aq_inner(self.context)      
        mylist = []    
        P = None
        currpath = self.request.VIRTUAL_URL_PARTS[1]
        
        for P in self.request.PARENTS:
            if P.getId()== "risq":
                break
        cnt = 0
        for l in linklist:
            cnt += 1
            ob = P.restrictedTraverse(l, None)
            state = False
            if ob is not None:
                obpath = "/".join(ob.getPhysicalPath())
                if currpath in obpath:
                    state = True
                mylist.append((ob, state, cnt))
            
        return mylist
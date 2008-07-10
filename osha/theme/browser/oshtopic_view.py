import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class OSHTopicView(BrowserView):
    """View for displaying the results of a topic outside the current context within the context
    """
    template = ViewPageTemplateFile('templates/oshtopic_view.pt')
    template.id = 'oshtopic-view'
    
    def __call__(self):
        topicpath = self.request.get('tp', '')
        if topicpath.startswith('/') and not topicpath.startswith('/osha/portal'):
            topicpath = topicpath[1:]
        self.tp = topicpath
        
        return self.template() 
        
    def getTopic(self):
        context = Acquisition.aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        topic = portal.restrictedTraverse(self.tp)
        return topic        
        
    def Title(self):
        return self.getTopic().Title()        

    def getText(self):
        return self.getTopic().getText()
        
    def Format(self):
        return self.getTopic().Format()        
        
    def queryCatalog(self):
        return self.getTopic().queryCatalog(batch=True)        

    def getCustomViewFields(self):
        return self.getTopic().getCustomViewFields()
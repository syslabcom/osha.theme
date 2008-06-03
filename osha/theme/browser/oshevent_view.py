import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class OSHEventView(BrowserView):
    """View for displaying events outside the current context within the context
    """
    template = ViewPageTemplateFile('templates/oshevent_view.pt')
    
    def __call__(self):
        topicpath = self.request.get('tp', '')
        if topicpath.startswith('/'):
            topicpath = topicpath[1:]
        context = Acquisition.aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        self.topic = portal.restrictedTraverse(topicpath)
        
        return self.template() 
        
    def Title(self):
        return self.topic.Title()        

    def getText(self):
        return self.topic.getText()
        
    def Format(self):
        return self.topic.Format()        
        
    def queryCatalog(self):
        return self.topic.queryCatalog(batch=True)        

    def getCustomViewFields(self):
        return self.topic.getCustomViewFields()
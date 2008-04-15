import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class WorklistView(BrowserView):
    """View for displaying the worklist (filter plus result list)
    """
    template = ViewPageTemplateFile('templates/worklist.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)

        return self.template() 
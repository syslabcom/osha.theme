from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class TopicsView(BrowserView):
    """ View class for /topics 
    """
    template = ViewPageTemplateFile('templates/topics_view.pt')
    template.id = "topics-view"    

    def __call__(self):
        return self.template() 
        


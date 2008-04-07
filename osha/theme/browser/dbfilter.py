from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class DBFilterView(BrowserView):
    """View for displaying the sep content filter page at /en/good_practice/topics/xx
    """
    template = ViewPageTemplateFile('templates/dbfilter.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)

        return self.template() 


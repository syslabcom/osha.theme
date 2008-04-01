from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class PublicationsSearchView(BrowserView):
    """View for displaying the publications overview page at /xx/publications
    """
    template = ViewPageTemplateFile('templates/publicationsearch.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)

        return self.template() 


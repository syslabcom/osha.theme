from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class SEPListingView(BrowserView):
    """View for displaying the dynamic SEP overview page at /topics, /sector, /priority_groups
    """
    template = ViewPageTemplateFile('templates/seplisting.pt')
    
    def __call__(self):
        return self.template() 

    def getAreaLinks(self):
        """ return the SEPS under topics """
        path = "/".join(self.context.getPhysicalPath())
        pc = getToolByName(self.context, 'portal_catalog')
        res = pc(path={'query': path, 'depth': 1}, portal_type=["Folder", "Large Plone Folder"], sort_on='sortable_title')
        
        return [x for x in res if not x.exclude_from_nav]
        
        

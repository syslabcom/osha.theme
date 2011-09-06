from Acquisition import aq_base
#from plone.memoize import ram
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class ResourceListingView(BrowserView):
    """View for displaying resources such as campaign materials
    """
    
    def __call__(self):
        self.request.set('disable_border', True)

        self.items = self._getItems()
        self.description = self.context.Description()
        if getattr(aq_base(self.context), 'content', None):
            content = getattr(self.context, 'content')
            if hasattr(content, 'getText') and callable(content.getText):
                self.description = content.getText()
        return self.index()

    def _getItems(self):
        pwt = getToolByName(self.context, 'portal_workflow')
        objects = [x for x in self.context.objectValues(['ATFile', 'ATImage', 'ATBlob'])
                if pwt.getInfoFor(x, 'review_state') == 'published' ]
        
        items = [dict(title=x.title_or_id(), description=x.Description(), link=x.absolute_url()) for x in objects]
        return items
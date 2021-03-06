#import Acquisition, time
#from plone.memoize import ram
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class FAQView(BrowserView):
    """View for displaying documents in FAQ style
    """
    
    def __call__(self):
        self.request.set('disable_border', True)
#        context = Acquisition.aq_inner(self.context)
        
#        portal_catalog = getToolByName(context, 'portal_catalog')
#        portal_languages = getToolByName(context, 'portal_languages')
#        self.lang = portal_languages.getPreferredLanguage()
        self.items = self._getItems()
        return self.index()

    def getName(self):
        return self.__name__

    def _getItems(self):
        pwt = getToolByName(self.context, 'portal_workflow')
        objects = [x for x in self.context.objectValues(['Document', 'RichDocument'])
                if pwt.getInfoFor(x, 'review_state') == 'published' ]
        
        items = [dict(title=x.Title(), text=x.getText(), link=x.absolute_url()) for x in objects]
        return items
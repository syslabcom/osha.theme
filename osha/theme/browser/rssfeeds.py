from zope.interface import Interface, implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class IRSSFeedsView(Interface):

    def type_feeds():
        """ return all feeds by typical types and offer subfeeds by keyword
        """
        
class RSSFeedsView(BrowserView):
    """View for displaying the site rss feeds
    """
    implements(IRSSFeedsView)

    template = ViewPageTemplateFile('templates/rssfeeds.pt')
    buttons = ViewPageTemplateFile('templates/rssfeed_helpers.pt')
           
    def __call__(self):    
        #self.request.set('disable_border', True)
        
        # XXX: We have to put this somewhere configurable. Where?
        self.TYPES = ['News Item', 'Event', 'Publication', 'PressRelease']
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        self.KEYWORDS = portal_catalog.uniqueValuesFor('Subject')
        
        return self.template()
        
    def type_feeds(self):
        """ return all feeds by typical types and offer subfeeds by keyword
        """
        portal_types = getToolByName(self.context, 'portal_types')
        portal_url = getToolByName(self.context, 'portal_url')
        portal_languages = getToolByName(self.context, 'portal_languages')

        L = []
        lang = portal_languages.getPreferredLanguage()
        portal_path = portal_url.getPortalPath()
        url_pattern = portal_path + \
            "/search_rss?portal_type=%s&Language=%s&review_state=published"
            
        for T in self.TYPES:                        
            ti = portal_types.getTypeInfo(T)
            if ti is None:
                continue
            L.append( dict(
                id=T, 
                title=ti.Title(), 
                icon=ti.getIcon(),
                url=url_pattern %(T,lang)
                ))
        return L
        
    def subject_feeds(self):
        """ return all feeds by keyword and offer subfeeds by type
        """
        portal_types = getToolByName(self.context, 'portal_types')
        portal_url = getToolByName(self.context, 'portal_url')
        portal_languages = getToolByName(self.context, 'portal_languages')

        L = []
        lang = portal_languages.getPreferredLanguage()
        portal_path = portal_url.getPortalPath()
        url_pattern = portal_path + \
            "/search_rss?Subject=%s&Language=%s&review_state=published"
            
        for T in self.KEYWORDS:  
            Title  = T.capitalize().replace("_", " ").replace("-", " ")                      
            L.append( dict(
                id=T, 
                title=Title, 
                icon='topic_icon.gif',
                url=url_pattern %(T,lang)
                ))
        return L
                    
    def quick_buttons(self, title, url):
        """ return a button row to quickly add the feed to popular syndication services
        """
        return self.buttons(title=title, url=url)



    def currlang(self):
        """ return the current language in pretty form
        """
        portal_languages = getToolByName(self.context, 'portal_languages')
        lang = portal_languages.getPreferredLanguage()
        return portal_languages.getNameForLanguageCode(lang)
        
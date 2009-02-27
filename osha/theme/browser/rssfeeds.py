from zope.interface import Interface, implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Products.PythonScripts.standard import url_quote

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
    TYPES = ['News Item', 'Event', 'Publication', 'PressRelease']
    
    def __call__(self):
        return self.template()
        
    def type_feeds(self):
        """ return all feeds by typical types and offer subfeeds by keyword
        """
        portal_types = getToolByName(self.context, 'portal_types')
        portal_url = getToolByName(self.context, 'portal_url')
        portal_languages = getToolByName(self.context, 'portal_languages')

        L = []
        lang = portal_languages.getPreferredLanguage()
        portal_path = portal_url.getPortalObject().absolute_url()
        url_pattern = portal_path + "/search_rss?portal_type=%s&Language=%s&review_state=published&sort_on=%s"
                        
        for T in self.TYPES:
            if T == 'Event':
                sorter="start"
            else:
                sorter = "effective"
            ti = portal_types.getTypeInfo(T)
            if T == 'Publication':
                url = url_pattern %('File',lang, sorter)
                url += '&object_provides=slc.publications.interfaces.IPublicationEnhanced'
                L.append( dict(
                    id=T, 
                    title=T.capitalize()+'s', 
                    icon='publication_icon.gif',
                    url=url
                    ))
            elif T in ('News Item', 'Event'):
                now = DateTime().strftime('%Y/%m/%d %H:%M')
                url = url_pattern %(T,lang, sorter)
                url += '&effective=%(date)s&effective_usage=range:max&expires=%(date)s&expires_usage=range:min' % dict(date=url_quote(now))
                L.append( dict(
                    id=T, 
                    title=ti.Title()+'s', 
                    icon=ti.getIcon(),
                    url=url
                    ))
            elif ti is None:
                continue
            else:
                L.append( dict(
                    id=T, 
                    title=ti.Title()+'s', 
                    icon=ti.getIcon(),
                    url=url_pattern %(T,lang, sorter)
                    ))
        return L
        
    def subject_feeds(self):
        """ return all feeds by keyword and offer subfeeds by type
        """
        oshaview = self.context.restrictedTraverse('@@oshaview')
        CATS = oshaview.getTranslatedCategories()
        
        portal_types = getToolByName(self.context, 'portal_types')
        portal_url = getToolByName(self.context, 'portal_url')
        portal_languages = getToolByName(self.context, 'portal_languages')

        L = []
        lang = portal_languages.getPreferredLanguage()
        portal_path = portal_url.getPortalPath()
        url_pattern = portal_path + \
            "/search_rss?Subject=%s&Language=%s&review_state=published&sort_on=effective"
            
        for T, Title in CATS:  
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
        
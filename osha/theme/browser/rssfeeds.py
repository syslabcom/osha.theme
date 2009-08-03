from zope.interface import Interface, implements
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from types import UnicodeType

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
                url = portal_path + "/%s/events/RSS" % lang
            elif T == 'News Item':
                url = portal_path + "/%s/news/RSS" % lang
            else:
                sorter = "effective"
                url = url_pattern %(T,lang, sorter)
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
            elif ti is None:
                continue
            else:
                L.append( dict(
                    id=T, 
                    title=ti.Title()+'s', 
                    icon=ti.getIcon(),
                    url=url
                    ))
        return L
        
    def _getTranslatedCategories(self):
        """
        Return list of tuples, tuple 1 is the category id, tuple 2 the title
        of the category"""
        oshaview = self.context.restrictedTraverse('@@oshaview')
        CATS = oshaview.getTranslatedCategories()        
    
    def _getPortalPath(self):
        return getToolByName(self.context, 'portal_url').getPortalPath()
    
    def _getPrefferedLanguage(self):
        return getToolByName(self.context, 'portal_languages').getPreferredLanguage()
    
    def subject_feeds(self):
        url_pattern = self._getPortalPath() + "/search_rss?Subject=%(id)s&RSSTitle=%(title)s&Language=%(lang)s&review_state=published&sort_on=effective"
        retval = []
        lang = self._getPrefferedLanguage()
        for id, title in self._getTranslatedCategories():
            retval.append(dict(
                id=id, 
                title=title, 
                icon='topic_icon.gif',
                url=url_pattern %(dict(title=title, id=id, lang=lang))
                ))
        return retval
                    
    def quick_buttons(self, title, url):
        """ return a button row to quickly add the feed to popular syndication services
        """
        if isinstance(title, UnicodeType):
            title = title.encode('utf-8')
        return self.buttons(title=title, url=url)



    def currlang(self):
        """ return the current language in pretty form
        """
        portal_languages = getToolByName(self.context, 'portal_languages')
        lang = portal_languages.getPreferredLanguage()
        return portal_languages.getNameForLanguageCode(lang)
        
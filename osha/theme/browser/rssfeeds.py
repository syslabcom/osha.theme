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
    TYPES = {'News Item'    : "/%%(lang)s/events/RSS?RSSTitle=%(title)s", 
             'Event'        : "/%%(lang)s/news/RSS?RSSTitle=%(title)s", 
             'Publication'  : "/search_rss?RSSTitle=%(title)s&portal_type=Publication&Language=%%(lang)s&review_state=published&sort_on=%%(sorter)s",
             'PressRelease' : "/search_rss?RSSTitle=%(title)s&portal_type=PressRelease&Language=%%(lang)s&review_state=published&sort_on=%%(sorter)s&object_provides=slc.publications.interfaces.IPublicationEnhanced"}
    
    def __call__(self):
        return self.template()
    
    def _getTypesForFeeds(self):
        """
        Return a list with dictionaries with information about types, just 
        enough for rss feed generation:
        doc_type
        title: Thats something beautiful for RSS
        icon
        base_url = That is the template for generating correct rss for the type
                   The template needs the following variables:
                   lang
                   sorter: sort order
        """
        portal_types = getToolByName(self.context, 'portal_types')

        for doc_type, type_url in self.TYPES.items():
            if doc_type == 'Publication':
                title = doc_type.capitalize() + 's'
                yield dict(doc_type=doc_type, title=title, 
                           icon="publication_icon.gif", base_url = type_url % {'title' : title})        
            else:
                ti = portal_types.getTypeInfo(doc_type)
                if ti:
                    title = ti.Title()+'s'
                    yield dict(doc_type=doc_type, title=title,
                               icon=ti.getIcon(),base_url=type_url % {'title' : title})
                    
    def type_feeds(self):
        """ return all feeds by typical types and offer subfeeds by keyword
        """

        retval = []
        lang = self._getPrefferedLanguage()
        portal_path = self._getPortalPath()
                        
        for type in self._getTypesForFeeds():
            url = portal_path + type['base_url'] % dict(lang=lang, sorter="effective")
            
            retval.append( dict(
                    id=type['doc_type'], 
                    title=type['title'], 
                    icon=type['icon'],
                    url=url
                    ))
        return retval
        
    def _getTranslatedCategories(self):
        """
        Return list of tuples, tuple 1 is the category id, tuple 2 the title
        of the category"""
        oshaview = self.context.restrictedTraverse('@@oshaview')
        return oshaview.getTranslatedCategories()        
    
    def _getPortalPath(self):
        return getToolByName(self.context, 'portal_url').getPortalObject().absolute_url()
    
    def _getPrefferedLanguage(self):
        return getToolByName(self.context, 'portal_languages').getPreferredLanguage()
    
    def subject_feeds(self):
        url_pattern = self._getPortalPath() + u"/search_rss?Subject=%(id)s&RSSTitle=%(title)s&Language=%(lang)s&review_state=published&sort_on=effective"
        retval = []
        lang = self._getPrefferedLanguage()
        for id, title in self._getTranslatedCategories():
            retval.append(dict(
                id=id, 
                title=title, 
                icon='topic_icon.gif',
                url=(url_pattern %(dict(title=title, id=id, lang=lang))).encode('utf-8'),
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
        
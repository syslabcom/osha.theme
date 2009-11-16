from Acquisition import aq_inner, aq_parent
from Products.AdvancedQuery import In, Eq, Ge, Le, And, Or, Generic
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from osha.theme.browser.dbfilter import DBFilterView
from Products.CMFPlone.PloneFolder import PloneFolder 

class MediaLibraryTagEventView(BrowserView):
    """ View to redirect to the bulk tagger for an event
    """
    def __call__(self):
        event = self.request.get('event', '')
        return "ok, selected event %s" % event

class MediaLibraryView(BrowserView):
    """View for the media Library
    """
    template = ViewPageTemplateFile('templates/media_library.pt')
    template.id = "media-library"
    
    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()
        
    def taggable_events(self):
        folders = self.context.contentValues(filter={'portal_type':['Folder', 'Large Plone Folder']})
        folders.sort(lambda x,y: cmp(x.Title(),y.Title()) )
        for folder in folders:
            yield dict(value=folder.getId(), content=folder.Title())
    
class MediaLibraryUploadView(BrowserView):
    """ View to create the appropriate folder
    """
    
    def __call__(self):
        """ create the folder and configure it depending on the button pressed
        """
        
        type_name = "Folder"
        id = self.context.generateUniqueId(type_name)
        new_id = self.context.invokeFactory(id=id, type_name=type_name)

        folder = getattr(self.context, new_id)
        folder.processForm(self.request)

        if self.request.get('form.button.add_image_folder', None):
            pass
        elif self.request.get('form.button.add_audio_folder', None):
            pass
        elif self.request.get('form.button.add_video_folder', None):
            pass
        return self.request.RESPONSE.redirect("%s/flashupload" % folder.absolute_url())
            
            
class MediaLibrarySearchView(DBFilterView):
    """View for the media Library Search.
    
    This makes a specialised search form which is used to retrieve images from the 
    Digital Assets library.
    It searches only for images and files in the current section and
    shows the results as a gallery view.
    """

    template = ViewPageTemplateFile('templates/media_library_search.pt')
    template.id = "media-library-search"


    def __call__(self):
        self.request.set('disable_border', True)
        return self.template()

    def get_keyword(self):
        """ Return the first value from keywords/request or an empty string
        """
        keywords = self.request.get("keywords", "")
        keyword = ""
        if keywords:
            keyword = keywords[0]
        return keyword

    def buildQuery(self):
        """ Build the query based on the request.
        Overriding this method from DBFilter because it treats an
        empty keywords:list as a value causing nothing to be returned
        """
        context = aq_inner(self.context)
        query = In('portal_type', ['Image', 'File'])

        keywords = self.request.get('keywords', [])
        if keywords:
            if keywords !=  ['']:
                query = query & In('Subject', keywords)

        nace = list(self.request.get('nace', ''))
        if '' in nace:
            nace.remove('')
        if nace:
            query = query & In('nace', nace)
            #query.update({'nace':nace})

        multilingual_thesaurus = list(
            self.request.get('multilingual_thesaurus', '')
            )
        if '' in multilingual_thesaurus:
            multilingual_thesaurus.remove('')
        if multilingual_thesaurus:
            query = query & In('multilingual_thesaurus', multilingual_thesaurus)
            #query.update({'multilingual_thesaurus':multilingual_thesaurus})

        SearchableText = self.request.get('SearchableText', '')
        if SearchableText != '':
            query = query & Generic(
                'SearchableText',
                {'query': SearchableText, 'ranking_maxhits': 1000 }
                )
            #query.update({'SearchableText': {'query': SearchableText, 'ranking_maxhits': 10000 }})

        return query

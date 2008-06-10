import Acquisition
from plone.portlet.collection import collection
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from time import time
from plone.app.portlets.cache import get_language
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize

def render_cachekey(fun, self):
    """
    Generates a key based on:

    * Portal URL
    * Negotiated language
    * Anonymous user flag
    * Portlet manager
    * Assignment
    * URL of collection used (instead of using _data)
    
    """
    context = Acquisition.aq_inner(self.context)

    fingerprint = self.collection_url()
    anonymous = getToolByName(context, 'portal_membership').isAnonymousUser()

    key= "".join((
        getToolByName(Acquisition.aq_inner(self.context), 'portal_url')(),
        get_language(Acquisition.aq_inner(self.context), self.request),
        str(anonymous),
        self.manager.__name__,
        self.data.__name__,
        fingerprint))
    return key


class Renderer(collection.Renderer):
    """Portlet renderer.
    
    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """    
    _template = ViewPageTemplateFile('collection.pt')

#    @ram.cache(lambda *args: time() // (60 * 10))
    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @memoize
    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return None


        collectionpath = "/".join(collection.getPhysicalPath())
        
        context = Acquisition.aq_inner(self.context)
        if not context.isPrincipiaFolderish:
            context = Acquisition.aq_parent(context)
        contextpath = "/".join(context.getPhysicalPath())
        
        # If the shown collection is within the current context, reference it directly
        if collectionpath.startswith(contextpath):
            return collection.absolute_url()
        # If the collection is in a different place in the site, use the proxy view
        else:
            return "%s/@@oshtopic-view?tp=%s" % (context.absolute_url(), collectionpath)
            
            
    @memoize
    def getPath(self, ob):
        path = ob.getURL()
        context = Acquisition.aq_inner(self.context)
        portal_properties = getToolByName(context, 'portal_properties')
        viewtypes = portal_properties.site_properties.getProperty('typesUseViewActionInListings')
        if ob.portal_type in viewtypes:
            path = path+'/view'
        return path
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import search
from plone.app.portlets.cache import render_cachekey
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_inner

class Renderer(search.Renderer):
    """Dynamically override standard header for search portlet"""
    _template = ViewPageTemplateFile('defaultsearch.pt')

    def __init__(self, context, request, view, manager, data):
        search.Renderer.__init__(self, context, request, view, manager, data)

        self.language = getToolByName(self.context, 'portal_languages').getPreferredLanguage()

        osha_view = getMultiAdapter((context, request), name=u'oshaview')
        self.subsite_url = osha_view.subsiteRootUrl()
        self.subsite_path = osha_view.subsiteRootPath()

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        osha_view = getMultiAdapter((self.context, self.context.request), name=u'oshaview')
        subsite_url = osha_view.subsiteRootUrl()
        return (preflang, subsite_url)
        
    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def enable_livesearch(self):
        return False

    @memoize
    def _get_base_url(self):
        root = self.context.restrictedTraverse(self.subsite_path)
        if hasattr(aq_base(aq_inner(root)), self.language):
            return '%s/%s' %(self.subsite_url, self.language)
        else:
            return self.subsite_url

    def search_form(self):
        base_url = self._get_base_url()
        return '%s/search_form' % base_url

    def search_action(self):
        base_url = self._get_base_url()
        return '%s/search' % base_url

    def index_alphabetical(self):
        return '%s/%s/@@index_alphabetical' %(self.subsite_url, self.language)


    def showAtozLink(self):
        osha_view = getMultiAdapter((self.context, self.request), name=u'oshaview')
        show = osha_view.get_subsite_property('show_atoz_link')
        if show is None:
            show = True
        return show

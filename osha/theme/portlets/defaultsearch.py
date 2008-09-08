from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import search
from plone.app.portlets.cache import render_cachekey
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

class Renderer(search.Renderer):
    """Dynamically override standard header for search portlet"""
    _template = ViewPageTemplateFile('defaultsearch.pt')

    def __init__(self, context, request, view, manager, data):
        search.Renderer.__init__(self, context, request, view, manager, data)

        osha_view = getMultiAdapter((context, request), name=u'oshaview')
        self.subsite_url = osha_view.subsiteRootUrl()

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        return (preflang)
        
    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def enable_livesearch(self):
        return False

    def search_form(self):
        return '%s/search_form' % self.subsite_url

    def search_action(self):
        return '%s/search' % self.subsite_url

    def index_alphabetical(self):
        return '%s/%s/@@index_alphabetical' %(self.subsite_url, getToolByName(self.context, 'portal_languages').getPreferredLanguage())
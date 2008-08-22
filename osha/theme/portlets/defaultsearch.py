from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import search
from plone.app.portlets.cache import render_cachekey
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from time import time
from Products.CMFCore.utils import getToolByName

class Renderer(search.Renderer):
    """Dynamically override standard header for search portlet"""
    _template = ViewPageTemplateFile('defaultsearch.pt')

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        return (preflang)
        
    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def enable_livesearch(self):
        return False


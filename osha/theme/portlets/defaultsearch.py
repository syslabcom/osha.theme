from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import search
from plone.app.portlets.cache import render_cachekey
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from time import time

class Renderer(search.Renderer):
    """Dynamically override standard header for search portlet"""
    _template = ViewPageTemplateFile('defaultsearch.pt')


    #@ram.cache(lambda *args: time() // (60 * 60))
    def render(self):
        return xhtml_compress(self._template())

    def enable_livesearch(self):
        return False


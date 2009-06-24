from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from slc.googlesearch.portlets.searchbox import Renderer as BaseRenderer


class Renderer(BaseRenderer):
    """Dynamically override standard header for search portlet"""
    _template = ViewPageTemplateFile('googlesearchbox.pt')

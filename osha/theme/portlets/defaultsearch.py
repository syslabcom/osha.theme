from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.portlets.portlets import search

class Renderer(search.Renderer):
    """Dynamically override standard header for search portlet"""
    render = ViewPageTemplateFile('defaultsearch.pt')



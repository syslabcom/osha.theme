from plone.app.portlets.portlets import navigation

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class Renderer(navigation.Renderer):
    """Dynamically override standard header for risq navtree portlet"""
    
    _template = ViewPageTemplateFile('risqnavigation.pt')
    recurse = ViewPageTemplateFile('risqnavigation_recurse.pt')
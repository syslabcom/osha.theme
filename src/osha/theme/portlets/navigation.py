from plone.app.portlets.portlets import navigation
import time
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import component
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.memoize import ram

def get_language(context, request):
    portal_state = component.getMultiAdapter(
        (context, request), name=u'plone_portal_state')
    return portal_state.locale().getLocaleID()

def render_cachekey(fun, self):
    """
    Generates a key based on:

    * Portal URL
    * Negotiated language
    * Anonymous user flag
    * Portlet manager
    * Assignment
    * Fingerprint of the data used by the portlet
    
    """
    context = aq_inner(self.context)
    
    def add(brain):
        path = brain.getPath().decode('ascii', 'replace')
        return "%s\n%s\n\n" % (path, brain.modified)
    fingerprint = self.request.get('URL')
    member = getToolByName(context, 'portal_membership').getAuthenticatedMember()
    roles = member.getRoles()
    return "".join((
        get_language(aq_inner(self.context), self.request),
        str(roles),
        fingerprint))
        
        
class Renderer(navigation.Renderer):
    """Dynamically override standard header for navtree portlet"""
    
    _template = ViewPageTemplateFile('navigation.pt')
    recurse = ViewPageTemplateFile('navigation_recurse.pt')

    #@ram.cache(render_cachekey)
    def render(self):
        return self._template()
            
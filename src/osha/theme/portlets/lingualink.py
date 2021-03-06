import Acquisition
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.app.portlets.cache import render_cachekey

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

from Products.Five import BrowserView

class ILinguaLinkPortlet(IPortletDataProvider):    
    pass

class Assignment(base.Assignment):
    implements(ILinguaLinkPortlet)

    @property
    def title(self):
        return _(u"LinguaLink Portlet")

class Renderer(base.Renderer, BrowserView):

    _template = ViewPageTemplateFile('lingualink.pt')
    
    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        modified = self.context.modified()
        path = "/".join(self.context.getPhysicalPath())
        return (path, modified, preflang)
        
    # We MUST NOT use ram cache here. The LinguaLink portlet depends on freshness, because it needs to call performActions on every
    # page load, to check if the "create" link was clicked.
#    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.portal = portal_state.portal()
                
    @property
    def available(self):
        return self._data()
        
    def title(self):
        return _(u"LinguaLinks")
        
        
    @memoize
    def check_access(self):
        portal_membership = getToolByName(self.context, 'portal_membership')
        member = portal_membership.getAuthenticatedMember()
        return member is not None
        
    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(ILinguaLinkPortlet)
    label = _(u"Add LinguaLink Portlet")
    description = _(u"Manage LinguaLinks")

    def create(self):
        return Assignment()

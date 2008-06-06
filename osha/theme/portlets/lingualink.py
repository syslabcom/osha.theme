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

from Products.BlueLinguaLink.browser import LinguaLinkPortlet

class ILinguaLinkPortlet(IPortletDataProvider):    
    pass

class Assignment(base.Assignment):
    implements(ILinguaLinkPortlet)

    @property
    def title(self):
        return _(u"LinguaLink Portlet")

class Renderer(base.Renderer, LinguaLinkPortlet):

    _template = ViewPageTemplateFile('lingualink.pt')

    @ram.cache(render_cachekey)
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
        
        
    def check_access(self):
        portal_membership = getToolByName(self.context, 'portal_membership')
        member = portal_membership.getAuthenticatedMember()
        return member and member.hasRole('Manager')        
        
    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(ILinguaLinkPortlet)
    label = _(u"Add LinguaLink Portlet")
    description = _(u"Manage LinguaLinks")

    def create(self):
        return Assignment()

import Acquisition
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.cache import render_cachekey
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from time import time
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

class IAlertServicePortlet(IPortletDataProvider):
    
    pass

class Assignment(base.Assignment):
    implements(IAlertServicePortlet)

    @property
    def title(self):
        return _(u"Alert Service")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('alertservice.pt')

    @ram.cache(lambda *args: time() // (60 * 60))
    def render(self):
        return xhtml_compress(self._template())


    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        
        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()
        
    def icon(self):
        icon = self.portal.restrictedTraverse('portlet_alertservice_icon.gif')
        return icon.tag(title='Alert Service')

    @memoize
    def num_subscribers(self):
        context = Acquisition.aq_inner(self.context)
        portal_alerts = getToolByName(context, 'portal_alertservice')
        try:
            n = len(portal_alerts.nprofiles.objectIds())
        except:
            n=''
        return n
        
    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IAlertServicePortlet)
    label = _(u"Add Alert Service Portlet")
    description = _(u"Provides the link to updates on topics of your choice.")

    def create(self):
        return Assignment()

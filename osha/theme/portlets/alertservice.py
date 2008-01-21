from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

class IAlertServicePortlet(IPortletDataProvider):
    
    pass

class Assignment(base.Assignment):
    implements(IAlertServicePortlet)

    @property
    def title(self):
        return _(u"Alert Service")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('alertservice.pt')

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
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IAlertServicePortlet)
    label = _(u"Add Alert Service Portlet")
    description = _(u"Provides the link to updates on topics of your choice.")

    def create(self):
        return Assignment()

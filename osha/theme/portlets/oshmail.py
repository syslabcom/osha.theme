import Acquisition
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

class IOSHMailPortlet(IPortletDataProvider):
    
    pass

class Assignment(base.Assignment):
    implements(IOSHMailPortlet)

    @property
    def title(self):
        return _(u"Free Newsletter")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('oshmail.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        
        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()
        
    def icon(self):
        icon = self.portal.restrictedTraverse('portlet_newsletter_icon.png')
        return icon.tag(title='Free Newsletter')

    @memoize
    def num_subscribers(self):
        context = Acquisition.aq_inner(self.context)
        portal_properties = getToolByName(context, 'portal_properties')
        return portal_properties.site_properties.getProperty('num_subscribers_oshmail')

    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IOSHMailPortlet)
    label = _(u"Add Free Newsletter Portlet")
    description = _(u"Monthly review of strategic news.")

    def create(self):
        return Assignment()

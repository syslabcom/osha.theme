from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

class IEW2007Portlet(IPortletDataProvider):
    
    pass

class Assignment(base.Assignment):
    implements(IEW2007Portlet)

    @property
    def title(self):
        return _(u"European Campaign 2007")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('ew2007.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        
        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()
        
    def icon(self):
        icon = self.portal.restrictedTraverse('portlet_campaigns_ew2007_icon.gif')
        return icon.tag(title='European Campaign 2007')

    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IEW2007Portlet)
    label = _(u"Add EW2007 Portlet")
    description = _(u"European Campaign 2007")

    def create(self):
        return Assignment()

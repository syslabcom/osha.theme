from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

class IFirstTimePortlet(IPortletDataProvider):
    
    pass

class Assignment(base.Assignment):
    implements(IFirstTimePortlet)

    @property
    def title(self):
        return _(u"First time here?")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('firsttime.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        
        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()
        
    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IFirstTimePortlet)
    label = _(u"Add FirstTime Portlet")
    description = _(u"Provides the link to an overview over the site.")

    def create(self):
        return Assignment()

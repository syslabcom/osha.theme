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

class IFollowUsPortlet(IPortletDataProvider):
    pass

class Assignment(base.Assignment):
    implements(IFollowUsPortlet)

    @property
    def title(self):
        return _(u"Follow us on Twitter, LinkedIn etc.")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('follow_us.pt')

    def preflang(self):
        preflang = getToolByName(self,
                                 'portal_languages').getPreferredLanguage()
        return preflang

    def _render_cachekey(method, self):
        return (self.preflang())

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context,
                                        self.request),
                                       name=u'plone_portal_state')

        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()

    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IFollowUsPortlet)
    label = _(u"Follow us on Twitter, LinkedIn etc.")
    description = _(u"Provides links to social network "\
                    "sites such as Twitter, LinkedIn etc.")

    def create(self):
        return Assignment()

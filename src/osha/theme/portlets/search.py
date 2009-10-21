from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ISearchPortlet(IPortletDataProvider):
    """ A portlet displaying a (live) search box
    """

    enableLivesearch = schema.Bool(
            title = _(u"Enable LiveSearch"),
            description = _(u"Enables the LiveSearch feature, which shows "
                             "live results if the browser supports "
                             "JavaScript."),
            default = True,
            required = False)

class Assignment(base.Assignment):
    implements(ISearchPortlet)

    def __init__(self, enableLivesearch=True):
        self.enableLivesearch=enableLivesearch

    @property
    def title(self):
        return _(u"Search")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('search.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)

        osha_view = getMultiAdapter((context, request), name=u'oshaview')
        self.subsite_url = osha_view.subsiteRootUrl()

    def enable_livesearch(self):
        return self.data.enableLivesearch

    def search_form(self):
        return '%s/search_form' % self.subsite_url

    def search_action(self):
        return '%s/search' % self.subsite_url


class AddForm(base.AddForm):
    form_fields = form.Fields(ISearchPortlet)
    label = _(u"Add Search Portlet")
    description = _(u"This portlet shows a search box.")

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):
    form_fields = form.Fields(ISearchPortlet)
    label = _(u"Edit Search Portlet")
    description = _(u"This portlet shows a search box.")

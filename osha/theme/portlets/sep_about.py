from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _

class ISEPAboutPortlet(IPortletDataProvider):
    
    pass

class Assignment(base.Assignment):
    implements(ISEPAboutPortlet)

    @property
    def title(self):
        return _(u"Single Entry Point - About")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('sep_about.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        
        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()
        
    def sep_title(self):
        return self.context.Title()
        
    def about_documents(self):    
        return self.context.getFolderContents({'portal_type': 'Document'})
        
    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(ISEPAboutPortlet)
    label = _(u"Add Single Entry Point - About Portlet")
    description = _(u"Lists all static documents within the about folder of a single entry point.")

    def create(self):
        return Assignment()

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


class IMoreAboutPortlet(IPortletDataProvider):    
    pass

class Assignment(base.Assignment):
    implements(IMoreAboutPortlet)

    @property
    def title(self):
        return _(u"More About Portlet")

class Renderer(base.Renderer):

    render = ViewPageTemplateFile('moreabout.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        
        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()
        
    def title(self):
        return _(u"More about...")
        
    def editable(self):
        f = self._getfile()
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.checkPermission('Modify portal content', f)
        
    def editlink(self):
        f = self._getfile()
        return f.absolute_url()+'/edit'        
                
    def _getfile(self):
        context = Acquisition.aq_inner(self.context)
        portlet_moreabout = getattr(context, 'more-about', None)
        if portlet_moreabout is None:
            return None        
        return portlet_moreabout

    def content(self):
        return self._getfile() and self._getfile().getText() or None
        
    @memoize
    def _data(self):
        return True


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IMoreAboutPortlet)
    label = _(u"Add More-About Portlet")
    description = _(u"Display the contents of a file called portlet_moreabout")

    def create(self):
        return Assignment()

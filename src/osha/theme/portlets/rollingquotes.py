import random
import Acquisition
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface import IATFolder, IATBTreeFolder


class IRollingQuotesPortlet(IPortletDataProvider):    
    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)

    folder = schema.Choice(title=_(u"Folder"),
                                  description=_(u"Locate the Folder with quotes"),
                                  required=True,
                                  source=SearchableTextSourceBinder({'object_provides' : [IATFolder.__identifier__, IATBTreeFolder.__identifier__]},
                                                                    default_query='path:'))





class Assignment(base.Assignment):
    implements(IRollingQuotesPortlet)
    header = u""
    folder=None
    url = u""
    
    def __init__(self, header=u"", folder=None, url=u""):
        self.header = header
        self.folder = folder
        self.url = url

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header

    @property
    def getfolder(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.folder


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('rollingquotes.pt')
    
    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        return (preflang)

    #@ram.cache(_render_cachekey)
    def render(self):
        #return xhtml_compress(self._template())
        return self._template()
            
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')        
        self.portal = portal_state.portal()

    def title(self):
        return self.data.header

    def getFolder(self):
        folder = self.data.folder
        portal_url = getToolByName(self.context, 'portal_url')
        portal_path = portal_url.getPortalPath()
        return '%s%s'%(portal_path,folder)
        
    @memoize
    def fallback(self, ob, preflang):
        if ob is None:
            return None
        pref = ob.getTranslation(preflang)
        if not pref:
            canonical = ob.getCanonical()   
            return canonical
        return pref
        
    def getRandomObject(self):
        folder= self.data.folder
        portal_url=getToolByName(self.context, 'portal_url')
        portal_languages=getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()
        
        portal_path=portal_url.getPortalPath()
        folderob=self.context.restrictedTraverse('%s%s'%(portal_path,folder))
        folderlist = folderob.listFolderContents(contentFilter={"portal_type" : "News Item", "review_state" : "published" })
        ob = random.choice(folderlist)
        ob = self.fallback(ob, preflang)
        return ob




class AddForm(base.AddForm):
    form_fields = form.Fields(IRollingQuotesPortlet)
    label = _(u"Add Rolling Quotes Portlet")
    description = _(u"Display a Random Quote in the appropriate language with Language Fallback")
    form_fields['folder'].custom_widget = UberSelectionWidget
    
    def create(self, data):
        return Assignment(header=data.get('header', u""),
                          folder=data.get('folder', u"") )

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(IRollingQuotesPortlet)
    form_fields['folder'].custom_widget = UberSelectionWidget

    label = _(u"Rolling Quotes Portlet")
    description = _(u"This portlet displays a random Quote")

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
from Products.ATContentTypes.interface import IImageContent, IFileContent


class IImagePortlet(IPortletDataProvider):    
    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)

    image = schema.Choice(title=_(u"Image"),
                                  description=_(u"Locate the Image to show"),
                                  required=True,
                                  source=SearchableTextSourceBinder({'object_provides' : [IImageContent.__identifier__, IFileContent.__identifier__]},
                                                                    default_query='path:'))

    url = schema.TextLine(title=_(u"URL"),
                             description=_(u"URL around the image/flash"),
                             required=False)

    show_box = schema.Bool(title=_(u"Display Box?"),
                           description=_(u"Leave this unchecked if you only want to see your banner without a title and a box around."),
                            )

    width = schema.TextLine(title=_(u"Width"),
                             description=_(u"Enter display width"),
                             )
    height = schema.TextLine(title=_(u"Height"),
                              description=_(u"Enter display height"),
                              )


class Assignment(base.Assignment):
    implements(IImagePortlet)
    header = u""
    image=None
    url = u""
    show_box = False
    width='200'
    height='60'
    
    def __init__(self, header=u"", image=None, url=u"", show_box=False, width='200', height='60'):
        self.header = header
        self.image = image
        self.url = url
        self.show_box = show_box
        self.width = width
        self.height = height

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header
              

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('image.pt')
    flash_snippet = ViewPageTemplateFile('flashsnippet.pt')
    
    
    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        modified = self.get_object() and self.get_object().modified() or ''
        return (modified, preflang)

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())
            
    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')        
        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()
        
    @memoize
    def title(self):
        return self.data.header

    @memoize
    def url(self):
        if self.data.url:
            return "%s?sourceid=banner" % self.data.url
        return u''

    @memoize
    def show_box(self):
        return self.data.show_box

    @memoize
    def get_object(self):
        image_path = self.data.image
        if not image_path:
            return None

        if image_path.startswith('/'):
            image_path = image_path[1:]
        
        if not image_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        imgob = portal.restrictedTraverse(image_path, default=None)
        if not imgob:
            return None
            
        portal_languages = getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()
        
        if preflang != imgob.Language():
            if imgob.hasTranslation(preflang):
                return imgob.getTranslation(preflang)
            else:
                return imgob.getCanonical()
        return imgob
        
    @memoize
    def tag(self):
        ob = self.get_object()
        if hasattr(Acquisition.aq_base(ob), 'content_type'):
            typ = ob.content_type
        else:
            return ''
        try:
            major, minor = typ.split("/")
        except:
            major=""
            minor=""
        if typ=='application/x-shockwave-flash':
            return self.flash_snippet(url="%s?sourceid=banner" % ob.absolute_url(), width=self.data.width, height=self.data.height, alt=self.title(), title=self.title())
        elif major=='image':
            return self.get_object().tag(height=self.data.height, width=self.data.width, alt=self.title(), title=self.title())
        else:
            return ''
    
    
    @memoize
    def _data(self):
        return True


class AddForm(base.AddForm):
    form_fields = form.Fields(IImagePortlet)
    label = _(u"Add Image/Flash Portlet")
    description = _(u"Display an Image/Flash in the appropriate language with Language Fallback")
    form_fields['image'].custom_widget = UberSelectionWidget
    
    def create(self, data):
        return Assignment(header=data.get('header', u""),
                          image=data.get('image', u""),
                          url=data.get('url', u""),
                          show_box=data.get('show_box', True),
                          width=data.get('width', u""),
                          height=data.get('height', u""))

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(IImagePortlet)
    form_fields['image'].custom_widget = UberSelectionWidget

    label = _(u"Edit Image/Flash Portlet")
    description = _(u"This portlet displays an image/flash.")

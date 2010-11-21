import logging
from string import Template

import Acquisition

from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope import schema
from zope.i18n import translate

from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.ATContentTypes.interface import IImageContent, IFileContent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.PlacelessTranslationService import translate as pts_translate

log = logging.getLogger('osha.theme.portlets.image.py')


class IImagePortlet(IPortletDataProvider):
    header = schema.TextLine(
                        title=_(u"Portlet header"),
                        description=_(u"Title of the rendered portlet"),
                        required=True,
                        )
    image = schema.Choice(
                        title=_(u"Image"),
                        description=_(u"Locate the Image to show"),
                        required=True,
                        source=SearchableTextSourceBinder(
                            {'object_provides': [
                                            IImageContent.__identifier__,
                                            IFileContent.__identifier__,
                                            ]},
                            default_query='path:'),
                        )
    url = schema.TextLine(
                        title=_(u"URL"),
                        description=_(u"URL around the image/flash"),
                        required=False,
                        )
    width = schema.TextLine(
                        title=_(u"Width"),
                        description=_(u"Enter display width"),
                        required=False,
                        )
    height = schema.TextLine(
                        title=_(u"Height"),
                        description=_(u"Enter display height"),
                        required=False,
                        )
    show_box = schema.Bool(
                        title=_(u"Display box?"),
                        description=_(u"Leave this unchecked if you only want "
                            "to see your banner without a title and a box "
                            "around."),
                        )
    i18n_domain = schema.TextLine(
                        title=_(u"Translation domain?"),
                        description=_(u"Specify the tranlation domain "
                            "that this portlet will use. This determines "
                            "the value (if any) into which the title will "
                            "be translated."),
                        required=False,
                        )


class Assignment(base.Assignment):
    implements(IImagePortlet)
    header = u""
    image = None
    url = u""
    show_box = False
    width = '200'
    height = '60'
    i18n_domain = 'plone'

    def __init__(self, header=u"", image=None, url=u"", show_box=False,
                width='200', height='60', i18n_domain='plone'):

        self.header = header
        self.image = image
        self.url = url
        self.show_box = show_box
        self.width = width
        self.height = height
        self.i18n_domain = i18n_domain

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
        preflang = getToolByName(self.context,
            'portal_languages').getPreferredLanguage()

        modified = self.get_object() and self.get_object().modified() or ''
        header = self.title()
        path = self.data.image
        return (header, modified, preflang, path)

    @ram.cache(_render_cachekey)
    def render(self):
        try:
            return xhtml_compress(self._template())
        except AttributeError, e:
            log.error(e.__str__())
            return 'There was an error while rendering this portlet.'

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter(
                            (self.context, self.request),
                            name=u'plone_portal_state')
        self.portal = portal_state.portal()

    @property
    def available(self):
        return self._data()

    @memoize
    def title(self):
        lang = self.context.Language()
        # First we try with zope.i18n
        header = translate(
                    self.data.title,
                    domain=self.data.i18n_domain,
                    context=self.context.request,
                    target_language=lang,
                    default=self.data.title,
                    )

        # If that doesn't work, then it's back to old-school PTS
        if header == self.data.title:
            header = pts_translate(
                                self.data.i18n_domain,
                                self.data.title,
                                context=self.context,
                                target_language=lang,
                                default=self.data.title,
                                )
        return header

    @memoize
    def url(self):
        if self.data.url:
            if self.data.url.find('?') > 0:
                symbol = '&'
            else:
                symbol = '?'
            return "%s%ssourceid=banner&utm_source=home&utm_medium=banner&" \
                "utm_campaign=campaign" % (self.data.url, symbol)
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

        portal_state = getMultiAdapter(
                        (self.context, self.request),
                        name=u'plone_portal_state')
        portal = portal_state.portal()

        # XXX: unrestrictedTraverse cannot handle unicode :(
        if type(image_path) == unicode:
            image_path = str(image_path)

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
            major = ""
            minor = ""
        if typ == 'application/x-shockwave-flash':
            return self.flash_snippet()

        elif major == 'image':

            result = '<img src="%s"' % ob.absolute_url()
            title = getattr(self, 'title', '')
            result = '%s alt="%s title=%s"' % (result, title, title)

            width = True and self.data.width or "90%"
            result = '%s width="%s"' % (result, width)

            # % heights don't work well in webkit based browsers
            # but leaving out the height attribute works
            height = self.data.height
            if height:
                result = '%s height="%s"' % (result, height)
            return '%s />' % result
        else:
            return ''

    @memoize
    def _data(self):
        return True

    def flashcode(self):
        """ For an explanation of swfobject.js (2.*), see:
            http://code.google.com/p/swfobject/wiki/documentation
        """
        obj = self.get_object()
        obj_id = self.id_attr()
        flash = Template("""
        <div class="portletImage-flash">
            <object id="$id"
                    classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000"
                    width="$width"
                    height="$height"
                    altHtml="">
                <param name="movie" value="$data" />
                <!--[if !IE]>-->
                <object type="application/x-shockwave-flash"
                        data="$data"
                        width="$width"
                        height="$height">
                <!--<![endif]-->
                <div class="portletImage-flash"
                     i18n:translate=""
                     i18n:domain="osha">
                     You need the Adobe Flash Player to view this content.
                     <a href="http://get.adobe.com/flashplayer"
                        target="_blank">Download it from Adobe</a>
                </div>
                <!--[if !IE]>-->
                </object>
                <!--<![endif]-->
            </object>
        </div>
        <script type="text/javascript">
            swfobject.registerObject("$id", "7")
        </script>
        """)
        tal = flash.safe_substitute({
            'id': obj_id,
            'classid': obj_id,
            'width': self.data.width or "90%",
            'height': self.data.height or "60",
            'data': obj.absolute_url(),
            'movie': obj.getFile().filename,
            })
        return tal

    def id_attr(self):
        ob = self.get_object()
        return "flashobject-%s" % ob.UID()


class AddForm(base.AddForm):
    form_fields = form.Fields(IImagePortlet)
    label = _(u"Add Image/Flash Portlet")
    description = _(u"Display an Image/Flash in the appropriate language " \
        " with Language Fallback")
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

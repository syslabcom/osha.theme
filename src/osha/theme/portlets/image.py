import logging
from urlparse import urlparse
from string import Template

import Acquisition

from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.i18n import translate
from zope.interface import implements

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

log = logging.getLogger('osha.theme.portlets.image.py')


class IImagePortlet(IPortletDataProvider):
    header = schema.TextLine(
                        title=_(u"Portlet header"),
                        description=_(u"Title of the rendered portlet"),
                        required=True,
                        )
    image = schema.Choice(
                        title=_(u"Please specify an image or flash file,"),
                        required=False,
                        source=SearchableTextSourceBinder(
                            {'object_provides': [
                                            IImageContent.__identifier__,
                                            IFileContent.__identifier__,
                                            ]},
                            default_query='path:'),
                        )
    url = schema.TextLine(
                        title=_(u"and the web address which it should point to."),
                        description=_(u"You can optionally, give an URL here."
                                      u"The image will then be hyperlinked to "
                                      u"that URL"),
                        required=False,
                        )
    video_url = schema.TextLine(
                        title=_(u"Alternatively, please give a YouTube video's web address"),
                        description=_(u"Instead of choosing a specific Image "
                                      u"or Flash object from the OSHA database "
                                      u"and specifiying it above, "
                                      u"you can also paste here the web address of "
                                      u"a Youtube video."),
                        required=False,
                        default=u"",
                        )
    width = schema.TextLine(
                        title=_(u"Width"),
                        description=_(u"Enter display width"),
                        default=u'250',
                        required=True,
                        )
    height = schema.TextLine(
                        title=_(u"Height"),
                        description=_(u"Enter display height"),
                        default=u'190',
                        required=True,
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
    video_url = u""

    def __init__(self, 
                header=u"", 
                video_url=u"",
                image=None, 
                url=u"", 
                show_box=False,
                width='200', 
                height='60', 
                i18n_domain='plone'):

        self.video_url = video_url
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

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context,
            'portal_languages').getPreferredLanguage()

        modified = self.get_object() and self.get_object().modified() or ''
        header = self.title()
        path = self.data.image
        video_url = self.data.get('video_url')
        # http or https?
        protocol = self.request.get('SERVER_URL', '').split("://")[0]
        return (header, modified, preflang, path, video_url, protocol)

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

    def tag(self):
        ob = self.get_object()
        if not ob:
            if self.data.video_url:
                return self.video_code()
            else:
                raise AttributeError(u"Image/Flash portlet doesn't have "
                                    u"an object or video url specified")

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
            return self.flash_code()

        elif major == 'image':
            result = '<img src="%s"' % ob.absolute_url()
            if hasattr(self, 'title'):
                title = self.title()
            else:
                title = ''
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

    def video_code(self):
        """ Return the Youtube embed code
        """
        url = urlparse(self.data.video_url)
        url = [i for i in url if i != '']
        pars = url[-1].split('&')
        pars_dict = dict([p.split('=') for p in pars])
        if not pars_dict.has_key('v'):
            return "Error: could not generate video embed code"
        
        embed = Template("""
            <iframe title="$header" 
                    width="$width" 
                    height="$height"
                    src="https://www.youtube.com/embed/$video_id" 
                    frameborder="0"
                    allowfullscreen>
            </iframe>
        """)
        tal = embed.safe_substitute({
            'header': self.data.header,
            'video_id': pars_dict['v'],
            'width': self.data.width,
            'height': self.data.height,
            })
        return tal

    def flash_code(self):
        """ For an explanation of swfobject.js (2.*), see:
            https://code.google.com/p/swfobject/wiki/documentation
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
                     <a href="https://get.adobe.com/flashplayer"
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
        return Assignment(**data)

        
class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IImagePortlet)
    form_fields['image'].custom_widget = UberSelectionWidget

    label = _(u"Edit Image/Flash Portlet")
    description = _(u"This portlet displays an image/flash.")


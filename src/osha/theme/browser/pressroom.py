from five.formlib import formbase
from plone.app.portlets.portlets.rss import Assignment as RSSAssignment
from plone.app.portlets.portlets.rss import Renderer as RSSRenderer
from plone.memoize import ram
from Products.ATContentTypes.interface.document import IATDocument
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import isExpired
from Products.Five import BrowserView
from Products.Five.browser import pagetemplatefile
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser.textwidgets import TextWidget
from zope.annotation.interfaces import IAnnotations
from zope.component import getMultiAdapter
from zope.deprecation import deprecation
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
from zope.interface import implements

from osha.theme.browser.interfaces import IPressRoomConfiguration
from osha.theme.browser.interfaces import IPressRoomView
from osha.theme.config import FEED_KEY
from osha.theme.config import KEYWORDS_KEY
from osha.theme.config import PRESS_CONTACTS_KEY

import Acquisition

_ = MessageFactory('osha.theme')


class PressRoomView(BrowserView):
    implements(IPressRoomView)
    template = pagetemplatefile.ViewPageTemplateFile('templates/pressroom.pt')

    def __call__(self):
        #self.request.set('disable_border', True)
        return self.template()

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.result = []

    def _render_cachekey(method, self):
        return ('MemoNews')

    @ram.cache(_render_cachekey)
    @deprecation.deprecate("getFeed() is deprecated, use getRSSFeed instead.")
    def getFeed(self):
        context = Acquisition.aq_inner(self.context)
        sin = getToolByName(context, 'sin_tool')
        map = "MemoNews"
        rows = sin.sin(map, max_size=2)
        return rows

    def getRSSFeed(self, count=1000000):
        pp = getToolByName(self.context, 'portal_properties')
        op = getattr(pp, 'osha_properties', None)
        oshaview = getMultiAdapter(
            (self.context, self.request), name='oshaview')
        url = op and op.getProperty('osha_in_the_media_feed', '') or ''
        ass = RSSAssignment(
            portlet_title="",
            count=count,
            url=url
        )
        renderer = RSSRenderer(self.context, self.request, self, None, ass)
        renderer.update()
        for item in renderer.items:
            item['summary'] = oshaview.cropHtmlText(item['summary'], 500)
        return renderer

    @ram.cache(_render_cachekey)
    def getPresscontacts(self):
        context = Acquisition.aq_inner(self.context)
        canonical = context.getCanonical()
        contactInfo = list()
        folder = getattr(canonical, 'press-contacts')
        international = getattr(folder, 'international-press', None)
        if international:
            contactInfo.append(international)
        spanish = getattr(folder, 'spanish-press', None)
        if spanish:
            contactInfo.append(spanish)
        brussels = getattr(folder, 'brussels-liaison', None)
        if brussels:
            contactInfo.append(brussels)

        return contactInfo


class DynamicPressRoomView(BrowserView):
    implements(IPressRoomView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.result = []

    def _render_cachekey(method, self):
        return ('MemoNews')

    def getContext(self):
        context = Acquisition.aq_inner(self.context)
        # if dynamic-pressroom was used on a Document, get the parent-folder
        if IATDocument.providedBy(context):
            context = Acquisition.aq_parent(context)
        context = context.getCanonical()
        return context

    #@ram.cache(_render_cachekey)
    def get_feed(self):
        context = self.getContext()
        annotations = IAnnotations(context)
        if not annotations.get(FEED_KEY):
            return []
        keys = annotations[FEED_KEY]
        sin = getToolByName(context, 'sin_tool')
        rows = []
        for k in keys:
            rows += sin.sin(k, max_size=2)
        return rows

    #@ram.cache(_render_cachekey)
    def get_press_contacts(self):
        context = self.getContext()
        annotations = IAnnotations(context)
        contactInfo = list()
        if PRESS_CONTACTS_KEY in annotations:
            contact_paths = annotations[PRESS_CONTACTS_KEY]
            portal = context.portal_url.getPortalObject()
            for path in contact_paths:
                try:
                    contact = portal.unrestrictedTraverse(str(path))
                    contactInfo.append(contact)
                except AttributeError:
                    pass
        return contactInfo

    def get_press_subfolder_path(self, folder, lan=None):
        context = self.context
        pu = getToolByName(context, 'portal_url')
        portal = pu.getPortalObject()
        if lan is None:
            pl = getToolByName(context, 'portal_languages')
            lan = pl.getLanguageBindings()[0]
        return '/'.join(portal.getPhysicalPath() + (lan, 'press', folder))

    def get_press_subfolder(self, folder):
        path = self.get_press_subfolder_path(folder)
        try:
            return self.context.restrictedTraverse(path)
        except AttributeError:
            path = self.get_press_subfolder_path(folder, 'en')
            return self.context.restrictedTraverse(path)

    def get_press_releases(self):
        context = self.getContext()
        annotations = IAnnotations(context)
        cat = getToolByName(context, 'portal_catalog')
        sf = self.get_press_subfolder('press-releases')
        path = '/'.join(sf.getPhysicalPath())
        q = {
            'portal_type': 'PressRelease',
            'path': path,
            'sort_on': 'Date',
            'sort_order': 'reverse'
        }
        keywords = annotations.get(KEYWORDS_KEY)
        if keywords:
            q['Subject'] = keywords
        return cat(q)

    def get_articles(self):
        context = self.getContext()
        annotations = IAnnotations(context)
        cat = getToolByName(context, 'portal_catalog')
        sf = self.get_press_subfolder('articles')
        path = '/'.join(sf.getPhysicalPath())
        q = {
            'path': path,
            'sort_on': 'effective',
            'sort_order': 'reverse'
        }
        keywords = annotations.get(KEYWORDS_KEY)
        if keywords:
            q['Subject'] = keywords
        return cat(q)

    def get_audiovisual(self):
        context = self.getContext()
        annotations = IAnnotations(context)
        cat = getToolByName(context, 'portal_catalog')
        sf = self.get_press_subfolder('photos')
        path = '/'.join(sf.getPhysicalPath())
        q = {'path': path}
        keywords = annotations.get(KEYWORDS_KEY)
        if keywords:
            q['Subject'] = keywords
        return cat(q)


class KeywordWidget(TextWidget):
    """ Override TextWidget to increate the width
    """
    displayWidth = 80

kw_widget = CustomWidgetFactory(KeywordWidget)


class DynamicPressRoomConfigurationForm(formbase.PageForm):
    """ """
    form_fields = form.FormFields(IPressRoomConfiguration)
    form_fields['keyword_list'].custom_widget = kw_widget
    label = _(u"Configure this Press Room")

    def setUpWidgets(self, ignore_request=False):
        request = self.request
        if 'form.actions.save' in request:
            # Add annotated values to the request so that we see the saved
            # values on a freshly opened form.
            context = Acquisition.aq_inner(self.context).getCanonical()
            annotations = IAnnotations(context)
            for key in [PRESS_CONTACTS_KEY, FEED_KEY, KEYWORDS_KEY]:
                if annotations.get(key):
                    if key == KEYWORDS_KEY:
                        request.form['form.%s' % key] = ' '.join(
                            annotations[key])
                    elif key == PRESS_CONTACTS_KEY:
                        good_paths = list()
                        # safeguard against missing press contacts
                        for path in annotations[key]:
                            if path.startswith('/'):
                                path = path[1:]
                                try:
                                    context.restrictedTraverse(str(path))
                                    good_paths.append(path)
                                    request.form['form.%s' % key] = \
                                        annotations[key]
                                except AttributeError:
                                    pass
                        if len(good_paths) < len(annotations[key]):
                            annotations[key] = good_paths
                    else:
                        request.form['form.%s' % key] = annotations[key]

        self.adapters = {}
        self.widgets = form.setUpWidgets(
            self.form_fields, self.prefix, self.context, self.request,
            form=self, adapters=self.adapters, ignore_request=ignore_request)

    @form.action("save")
    def action_save(self, action, data):
        request = self.context.request
        context = Acquisition.aq_inner(self.context)
        canonical = context.getCanonical()
        annotations = IAnnotations(canonical)
        annotations[FEED_KEY] = data[FEED_KEY]
        if data[PRESS_CONTACTS_KEY]:
            annotations[PRESS_CONTACTS_KEY] = \
                        request.form.get('form.press_contacts', [])

        if data[KEYWORDS_KEY]:
            annotations[KEYWORDS_KEY] = \
                            (data[KEYWORDS_KEY]).strip().split(' ')
        else:
            annotations[KEYWORDS_KEY] = []

        return request.RESPONSE.redirect(
            '%s/@@dynamic-pressroom/' % '/'.join(context.getPhysicalPath()))

    @form.action("cancel")
    def action_cancel(self, action, data):
        context = Acquisition.aq_inner(self.context)
        return context.request.RESPONSE.redirect(
            '%s/@@dynamic-pressroom/' % '/'.join(context.getPhysicalPath()))


class PressReleasesView(BrowserView):

    def getResults(self):
        context = Acquisition.aq_inner(self.context)

        # try to get query parameters from Topic (if present)
        query = hasattr(context, 'buildQuery') and context.buildQuery()
        if not query:
            # otherwise construct a query
            query = dict(
                portal_type="PressRelease", sort_on='Date',
                sort_order='reverse', path='/'.join(context.getPhysicalPath()))

        search_view = self.context.restrictedTraverse(
            '@@language-fallback-search')
        results = search_view.search(query)
        # filter out results that are both outdated and expired
        to_show = [
            x for x in results if not (
                getattr(x, 'outdated', False) and isExpired(x))
        ]
        return to_show

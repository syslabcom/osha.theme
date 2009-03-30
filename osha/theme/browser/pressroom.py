from zope.annotation.interfaces import IAnnotations
from zope.app.form import CustomWidgetFactory
from zope.app.form.browser.textwidgets import TextWidget
from zope.component import getMultiAdapter, getUtility
from zope.formlib import form
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from zope.schema.fieldproperty import FieldProperty


import Acquisition
from OFS.SimpleItem import SimpleItem

from plone.memoize.instance import memoize
from plone.memoize import ram

from Products.CMFCore.utils import getToolByName
from Products.Five.browser import pagetemplatefile 
from Products.Five.formlib import formbase
from Products.Five import BrowserView

from osha.theme.browser.interfaces import IPressRoomView
from osha.theme.browser.interfaces import IPressRoomConfiguration
from osha.theme.config import FEED_KEY
from osha.theme.config import PRESS_CONTACTS_KEY
from osha.theme.config import KEYWORDS_KEY

from interfaces import IPressRoomConfiguration

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
        return ('meltwater')
    
    @ram.cache(_render_cachekey)
    def getFeed(self):
        context = Acquisition.aq_inner(self.context)
        sin = getToolByName(context, 'sin_tool')
        map = "meltwater"
        rows = sin.sin(map, max_size=2)
        return rows
        
        
class DynamicPressRoomView(BrowserView):
    implements(IPressRoomView)
    template = pagetemplatefile.ViewPageTemplateFile('templates/pressroom_dynamic.pt')

    def __call__(self):
        #self.request.set('disable_border', True)
        return self.template()

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.result = []
    
    def _render_cachekey(method, self):
        return ('meltwater')
    
    #@ram.cache(_render_cachekey)
    def getFeed(self):
        context = Acquisition.aq_inner(self.context)
        canonical = context.getCanonical()
        annotations = IAnnotations(canonical)
        if not annotations.get(FEED_KEY):
            return []
        keys = annotations[FEED_KEY]
        sin = getToolByName(context, 'sin_tool')
        rows = []
        for k in keys:
            rows += sin.sin(k, max_size=2)        
        return rows        

    #@ram.cache(_render_cachekey)
    def getPressContacts(self):
        context = Acquisition.aq_inner(self.context).getCanonical()
        annotations = IAnnotations(context)
        contact_paths = annotations[PRESS_CONTACTS_KEY]
        portal = context.portal_url.getPortalObject()
        return [portal.unrestrictedTraverse(str(path)) for path in contact_paths]

    #@ram.cache(_render_cachekey)
    def getKeywords(self):
        context = Acquisition.aq_inner(self.context).getCanonical()
        annotations = IAnnotations(context)
        return annotations[KEYWORDS_KEY]



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
        if not request.has_key('form.actions.save'):
            # Add annotated values to the request so that we see the saved 
            # values on a freshly opened form.
            context = Acquisition.aq_inner(self.context).getCanonical()
            annotations = IAnnotations(context)
            for key in [PRESS_CONTACTS_KEY, FEED_KEY, KEYWORDS_KEY]:
                if annotations.get(key):
                    if key == KEYWORDS_KEY:
                        request.form['form.%s' % key] =  ' '.join(annotations[key])
                    else:
                        request.form['form.%s' % key] =  annotations[key]

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
        annotations[KEYWORDS_KEY] = \
                        (data[KEYWORDS_KEY] or '').strip().split(' ')
        return request.RESPONSE.redirect(
                        '%s/@@dynamic-pressroom' % context.absolute_url())

    @form.action("cancel")
    def action_save(self, action, data):
        context = Acquisition.aq_inner(self.context)
        return request.RESPONSE.redirect(
                        '%s/@@dynamic-pressroom' % context.absolute_url())




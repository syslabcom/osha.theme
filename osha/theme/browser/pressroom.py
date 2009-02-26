import Acquisition
from zope.interface import implements
from osha.theme.browser.interfaces import IPressRoomView
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from plone.memoize.instance import memoize
from plone.memoize import ram
from zope.component import getMultiAdapter, getUtility
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PressRoomView(BrowserView):
    implements(IPressRoomView)
    template = ViewPageTemplateFile('templates/pressroom.pt')

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
    template = ViewPageTemplateFile('templates/pressroom_dynamic.pt')

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
        sin = getToolByName(context, 'sin_tool')
        map = "meltwater"
        rows = sin.sin(map, max_size=2)        
        return rows        

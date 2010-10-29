from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from slc.googlesearch.portlets.searchbox import Renderer as BaseRenderer
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_inner


class Renderer(BaseRenderer):
    """Dynamically override standard header for search portlet"""
    _template = ViewPageTemplateFile('googlesearchbox.pt')
    
    def __init__(self, context, request, view, manager, data):
        BaseRenderer.__init__(self, context, request, view, manager, data)
        osha_view = getMultiAdapter((self.context, self.request), name=u'oshaview')
        self.subsite_url = osha_view.subsiteRootUrl()
        self.subsite_path = osha_view.subsiteRootPath()

    def index_alphabetical(self):
        return '%s/%s/@@index_alphabetical' %(self.subsite_url, self.language)

    def showAtozLink(self):
        osha_view = getMultiAdapter((self.context, self.request), name=u'oshaview')
        show = osha_view.get_subsite_property('show_atoz_link')
        if show is None:
            show = True
        return show

    def oshGlobalSearchLink(self):
        return '%s/%s/slc_cse_search_results?&q=&cof=FORID:11&sa=Search&ie=UTF-8&cref=http://osha.europa.eu/google/international_cse.xml' %(self.subsite_url, self.language)

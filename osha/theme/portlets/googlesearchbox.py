from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from slc.googlesearch.portlets.searchbox import Renderer as BaseRenderer
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_inner


class Renderer(BaseRenderer):
    """Dynamically override standard header for search portlet"""
    _template = ViewPageTemplateFile('googlesearchbox.pt')
    
    
    
    def index_alphabetical(self):
        self.language = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        osha_view = getMultiAdapter((self.context, self.request), name=u'oshaview')
        self.subsite_url = osha_view.subsiteRootUrl()
        self.subsite_path = osha_view.subsiteRootPath()
        return '%s/%s/@@index_alphabetical' %(self.subsite_url, self.language)


    def showAtozLink(self):
        osha_view = getMultiAdapter((self.context, self.request), name=u'oshaview')
        show = osha_view.get_subsite_property('show_atoz_link')
        if show is None:
            show = True
        return show
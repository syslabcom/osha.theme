import logging

from Acquisition import aq_inner, aq_parent
from DateTime import DateTime

from zope.component import getMultiAdapter

from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import news

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize

from Products.AdvancedQuery import Or, Eq, And, In, Le
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

log = logging.getLogger('osha.theme/portlets/news.py')


class Renderer(news.Renderer):
    """Dynamically override standard header for news portlet"""
    
    _template = ViewPageTemplateFile('news.pt')
    
    #def _render_cachekey(method, self):
    #    preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
    #    portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
    #    navigation_root_path = portal_state.navigation_root_path()
    #    return (preflang, navigation_root_path)
    
    # Add respect to INavigationRoot
    # Add support for isNews flag
    
    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template()) 

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        if hasattr(catalog, 'getZCatalog'):
            catalog = catalog.getZCatalog()
        portal_languages = getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()

        # search in the navigation root of the currently selected language and in the canonical path
        # with Language = preferredLanguage or neutral
        paths = list()
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        paths.append(navigation_root_path)
        try:
            navigation_root = portal_state.portal().restrictedTraverse(navigation_root_path)
            canonical_path = '/'.join(navigation_root.getCanonical().getPhysicalPath())
            paths.append(canonical_path)
        except:
            pass

        oshaview = getMultiAdapter((self.context, self.request), name=u'oshaview')
        mySEP = oshaview.getCurrentSingleEntryPoint()
        kw = ''
        if mySEP is not None:
            kw = mySEP.getProperty('keyword', '')
            
        limit = self.data.count
        state = self.data.state
        
        queryA = Eq('portal_type', 'News Item')
        queryB = Eq('isNews', True)
        queryBoth = In('review_state', state) & In('path', paths) & In('Language', ['', preflang])
        if kw !='':
            queryBoth = queryBoth & In('Subject', kw)
        queryEffective = Le('effective', DateTime())
        query = And(Or(queryA, queryB), queryBoth, queryEffective)
        try:
            return catalog.evalAdvancedQuery(query, (('Date', 'desc'),) )[:limit]
        except KeyError, e:
            log.error('KeyError: %s' %  e.__str__())
            return []


    @memoize
    def all_news_link(self):
        context = aq_inner(self.context)
        if not context.isPrincipiaFolderish:
            context = aq_parent(context)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_url = portal_state.navigation_root_url()
        return '%s/news' % navigation_root_url


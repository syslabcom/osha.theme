from plone.app.portlets.portlets import events
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from Acquisition import aq_inner, aq_parent
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

class Renderer(events.Renderer):
    """Dynamically override standard header for news portlet"""
    
    _template = ViewPageTemplateFile('events.pt')

    # Add respect to INavigationRoot
    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
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
        query = dict(portal_type='Event',
                       review_state=state,
                       path=paths,
                       end={'query': DateTime(),
                            'range': 'min'},
                       sort_on='start',
                       Language=['', preflang],
                       sort_limit=limit)
        if kw !='':
            query.update(Subject=kw)
        return catalog(query)[:limit]


    @memoize
    def all_events_link(self):
        context = aq_inner(self.context)
        if not context.isPrincipiaFolderish:
            context = aq_parent(context)
        return '%s/oshevent-view' % context.absolute_url()

    @memoize
    def prev_events_link(self):
        context = aq_inner(self.context)
        if not context.isPrincipiaFolderish:
            context = aq_parent(context)        
        return '%s/oshevent-view?show=previous' % context.absolute_url()
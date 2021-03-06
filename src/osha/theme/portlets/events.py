from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from zope.component import getMultiAdapter
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.app.portlets.portlets import events
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class Renderer(events.Renderer):
    """ """
    _template = ViewPageTemplateFile('events.pt')

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        return (preflang, navigation_root_path)

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

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
        query = dict(portal_type=['Event'],
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
    def calendarLink(self):
        """ Compute a link to the "closest" calendar
        """
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        query = dict(portal_type="Folder",
                    path=navigation_root_path,
                    object_provides="p4a.calendar.interfaces.ICalendarEnhanced"
                    )
        res = catalog(query)
        if len(res):
            calurl = None
            pathelems = 0
            for r in res:
                pe = len(r.getPath().split('/'))
                if pathelems==0 or pe < pathelems:
                    calurl = r.getURL()
                    pathelems = pe
            return calurl
        return ""

    @memoize
    def all_events_link(self):
        calurl = self.calendarLink()
        if calurl:
            return '%s/events.html' % calurl
        else:
            context = aq_inner(self.context)
            if not context.isPrincipiaFolderish:
                context = aq_parent(context)
            return '%s/events.html' % context.absolute_url()

    @memoize
    def prev_events_link(self):
        calurl = self.calendarLink()
        if calurl:
            return '%s/past_events.html' % calurl
        else:
            context = aq_inner(self.context)
            if not context.isPrincipiaFolderish:
                context = aq_parent(context)        
            return '%s/past_events.html' % context.absolute_url()


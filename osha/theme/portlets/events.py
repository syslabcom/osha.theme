from plone.app.portlets.portlets import events
from DateTime import DateTime
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize.instance import memoize
from Acquisition import aq_inner
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
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        limit = self.data.count
        state = self.data.state
        return catalog(portal_type='Event',
                       review_state=state,
                       path=navigation_root_path,
                       end={'query': DateTime(),
                            'range': 'min'},
                       sort_on='start',
                       sort_limit=limit)[:limit]

from plone.app.portlets.portlets import events

from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

import Acquisition
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget


class IEventsPortlet(IPortletDataProvider):
    count = schema.Int(title=_(u'Number of items to display'),
                       description=_(u'How many items to list.'),
                       required=True,
                       default=5)

    state = schema.Tuple(title=_(u"Workflow state"),
                         description=_(u"Items in which workflow state to show."),
                         default=('published', ),
                         required=True,
                         value_type=schema.Choice(
                             vocabulary="plone.app.vocabularies.WorkflowStates")
                         )

    subject = schema.Tuple(title=_(u"Categories"),
                            description=_(u"Pick one or more categories for which you want to show events."),
                            default=tuple(),
                            required=False,
                            value_type=schema.Choice(
                                vocabulary="osha.policy.vocabularies.categories")
                            )

    target_calendar = schema.Choice(title=_(u"Target calendar"),
                                  description=_(u"Select a calendar where event-listings and the calendar view will be displayed. If you make a Topic into a calendar, only events matching its criteria will be displayed."),
                                  required=True,
                                  source=SearchableTextSourceBinder({'object_provides' : 'p4a.calendar.interfaces.ICalendarEnhanced'},
                                                                    default_query='path:'))
class Assignment(base.Assignment):
    implements(IEventsPortlet)

    def __init__(self, count=5, state=('published', ), subject=tuple(), target_calendar=None):
        self.count = count
        self.state = state
        self.subject = subject
        self.target_calendar = target_calendar

    @property
    def title(self):
        return _(u"Events")

class Renderer(events.Renderer):
    """Dynamically override standard header for news portlet"""

    _template = ViewPageTemplateFile('events.pt')

    def __init__(self, *args):
        events.Renderer.__init__(self, *args)
        context = Acquisition.aq_base(self.context)
        portal_languages = getToolByName(self.context, 'portal_languages')
        self.preflang = portal_languages.getPreferredLanguage()

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        target_calendar = self.data.target_calendar
        subject = self.data.subject
        return (target_calendar, preflang, subject)

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())


    # Add respect to INavigationRoot
    @memoize
    def _data(self):
        context = Acquisition.aq_inner(self.context)
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
        subject = list(self.data.subject)

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
        # If a subject is selected, use that for the query and disregard the NavigationRoot
        if len(subject):
            query.update(Subject=subject)
            del query['path']
        return catalog(query)[:limit]


    @memoize
    def getCalendar(self):
        """ get the calendar the portlet is pointing to
            fall back to the canonical if language version cannot be found
        """
        calendar_path = self.data.target_calendar
        if not calendar_path:
            return None

        if calendar_path.startswith('/'):
            calendar_path = calendar_path[1:]
        
        if not calendar_path:
            return None

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.restrictedTraverse(calendar_path, default=None)


    @memoize
    def fallback(self, preflang):
        cal = self.getCalendar()
        if cal is None:
            return None
        pref = cal.getTranslation(preflang)
        if not pref:
            canonical = cal.getCanonical()   
            return canonical
        return pref

    @memoize
    def all_events_link(self):
        f = self.fallback(self.preflang)
        if f is None:
            return ''
        return '%s/events.html' % f.absolute_url()

    @memoize
    def prev_events_link(self):
        f = self.fallback(self.preflang)
        if f is None:
            return ''
        return '%s/past_events.html' % f.absolute_url()


class AddForm(base.AddForm):
    form_fields = form.Fields(IEventsPortlet)
    form_fields['target_calendar'].custom_widget = UberSelectionWidget
    
    label = _(u"Add Events Portlet")
    description = _(u"This portlet lists upcoming Events.")

    def create(self, data):
        return Assignment(count=data.get('count', 5), 
            state=data.get('state', ('published',)),
            subject=data.get('subject', tuple()),
            target_calendar=data.get('target_calendar', None))

class EditForm(base.EditForm):
    form_fields = form.Fields(IEventsPortlet)
    form_fields['target_calendar'].custom_widget = UberSelectionWidget
    label = _(u"Edit Events Portlet")
    description = _(u"This portlet lists upcoming Events.")
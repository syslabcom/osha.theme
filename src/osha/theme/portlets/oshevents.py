from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

import Acquisition
from DateTime.DateTime import DateTime

from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets.cache import render_cachekey
from plone.app.portlets.portlets import base
from plone.app.portlets.portlets import events
from plone.app.vocabularies.catalog import SearchableTextSourceBinder

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from types import UnicodeType
from p4a.calendar.interfaces import ICalendarEnhanced


class IEventsPortlet(IPortletDataProvider):
    count = schema.Int(
            title=_(u'Number of items to display'),
            description=_(u'How many items to list.'),
            required=True,
            default=5
            )

    state = schema.Tuple(
            title=_(u"Workflow state"),
            description=_(u"Items in which workflow state to show."),
            default=('published', ),
            required=True,
            value_type=schema.Choice(
                vocabulary="plone.app.vocabularies.WorkflowStates")
            )

    subject = schema.Tuple(
            title=_(u"Categories"),
            description=_(u"Pick one or more categories for which you want to show events."),
            default=tuple(),
            required=False,
            value_type=schema.Choice(
                vocabulary="osha.policy.vocabularies.categories")
            )

    calendar_path = schema.TextLine(
            title=_(u'Target calendar path'),
            description=_(u"Enter a folder where the 'next / previous events' link will point to. This is optional"),
            required=False,
            )

    rss_path = schema.TextLine(
            title=_(u'RSS path'),
            description=_(u'Enter a relative path to the calendar or topic that displays an RSS representation of these events. "/RSS" will automatically be appended to the URL. This setting is optional'),
            required=False,
            )

    rss_explanation_path = schema.TextLine(
            title=_(u'RSS explanation path'),
            description=_(u'Enter a relative path to a page that gives general RSS information. This setting is optional.'),
            required=False,
            )


class Assignment(base.Assignment):
    implements(IEventsPortlet)

    def __init__(self, count=5, state=('published', ), subject=tuple(), calendar_path=None, rss_path='', rss_explanation_path=''):
        self.count = count
        self.state = state
        self.subject = subject
        self.calendar_path = calendar_path
        self.rss_path = rss_path
        self.rss_explanation_path = rss_explanation_path

    @property
    def title(self):
        return _(u"Events")

class Renderer(events.Renderer):
    """Dynamically override standard header for news portlet"""

    _template = ViewPageTemplateFile('oshevents.pt')

    def __init__(self, *args):
        events.Renderer.__init__(self, *args)
        portal_languages = getToolByName(self.context, 'portal_languages')
        self.preflang = portal_languages.getPreferredLanguage()

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.navigation_root_path = portal_state.navigation_root_path()
        portal = portal_state.portal()
        self.root = portal.restrictedTraverse(self.navigation_root_path)

        # backwards compatibility
        if not hasattr(self.data, 'calendar_path'):
            self.data.calendar_path=''
        if not hasattr(self.data, 'rss_path'):
            self.data.rss_path=''
        if not hasattr(self.data, 'rss_explanation_path'):
            self.data.rss_explanation_path=''

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        calendar_path = self.data.calendar_path
        subject = self.data.subject
        return (calendar_path, preflang, subject)

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())


    # Add respect to INavigationRoot
    @memoize
    def _data(self):
        context = Acquisition.aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        # search in the navigation root of the currently selected language and in the canonical path
        # with Language = preferredLanguage or neutral
        paths = list()
        paths.append(self.navigation_root_path)
        try:
            canonical_path = '/'.join(self.root.getCanonical().getPhysicalPath())
            paths.append(canonical_path)
        except:
            pass

        oshaview = getMultiAdapter((self.context, self.request), name=u'oshaview')
        mySEP = oshaview.getCurrentSingleEntryPoint()
        subject = list(self.data.subject)

        limit = self.data.count
        state = self.data.state
        query = dict(portal_type=['Event','SPSeminar'],
                       review_state=state,
                       path=paths,
                       end={'query': DateTime(),
                            'range': 'min'},
                       sort_on='start',
                       Language=['', self.preflang],
                       sort_limit=limit)
        # If a subject is selected, use that for the query and disregard the NavigationRoot
        if len(subject):
            query.update(Subject=subject)
            del query['path']
        return catalog(query)[:limit]


    @memoize
    def getCalendar(self, preflang):
        """ get the calendar the portlet is pointing to
            fall back to the canonical if language version cannot be found
        """
        calendar_path = self.data.calendar_path
        if not calendar_path:
            return None

        if calendar_path.startswith('/'):
            calendar_path = calendar_path[1:]
        
        if not calendar_path:
            return None

        if isinstance(calendar_path, UnicodeType):
            calendar_path = calendar_path.encode('utf-8')

        cal = self.root.restrictedTraverse(calendar_path, default=None)
        if not ICalendarEnhanced.providedBy(cal):
            cal = None
        # if the calendar is not found, and we are in a translated language tree:
        if cal is None and hasattr(self.root, 'isCanonical') \
                and not self.root.isCanonical():
            canroot = self.root.getCanonical()
            # ... look on the canonical root for the calendar
            cal = canroot.restrictedTraverse(calendar_path, default=None)
            # double check if a translated version in the preflang exists
            cal = cal and cal.getTranslation(preflang) or cal
        return cal


    @memoize
    def all_events_link(self):
        cal = self.getCalendar(self.preflang)
        if cal is None:
            return ''
        return '%s/events.html' % cal.absolute_url()

    @memoize
    def prev_events_link(self):
        cal = self.getCalendar(self.preflang)
        if cal is None:
            return ''
        return '%s/past_events.html' % cal.absolute_url()

    def showRSS(self):
        return bool(self.getRSSLink())

    def getRSSLink(self):
        if getattr(self.data, 'rss_path', None):
            rss_path = self.data.rss_path
            if rss_path.startswith('/'):
                rss_path = rss_path[1:]
            if isinstance(rss_path, UnicodeType):
                rss_path = rss_path.encode('utf-8')
            target = self.root.restrictedTraverse(rss_path, default=None)
            if target:
                return "%s/RSS" % target.absolute_url()
        return None

    def getRSSExplanationLink(self):
        if getattr(self.data, 'rss_explanation_path', None):
            rss_path = self.data.rss_explanation_path
            if rss_path.startswith('/'):
                rss_path = rss_path[1:]
            if isinstance(rss_path, UnicodeType):
                rss_path = rss_path.encode('utf-8')
            target = self.root.restrictedTraverse(rss_path, default=None)
            if target:
                return target.absolute_url()
        return None


class AddForm(base.AddForm):
    form_fields = form.Fields(IEventsPortlet)
    
    label = _(u"Add Events Portlet")
    description = _(u"This portlet lists upcoming Events.")

    def create(self, data):
        return Assignment(count=data.get('count', 5), 
            state=data.get('state', ('published',)),
            subject=data.get('subject', tuple()),
            calendar_path=data.get('calendar_path', None),
            rss_path=data.get('rss_path',''),
            rss_explanation_path=data.get('rss_explanation_path',''))

class EditForm(base.EditForm):
    form_fields = form.Fields(IEventsPortlet)
    label = _(u"Edit Events Portlet")
    description = _(u"This portlet lists upcoming Events.")

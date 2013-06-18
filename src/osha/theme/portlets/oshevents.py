import Acquisition
from collective.solr.mangler import iso8601date
from DateTime.DateTime import DateTime

from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets.portlets import base
from plone.app.portlets.portlets import events

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from types import UnicodeType

from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements


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
            description=_(
                    u"Pick one or more categories for which you want to show "
                    "events."),
            default=tuple(),
            required=False,
            value_type=schema.Choice(
                vocabulary="osha.policy.vocabularies.categories")
            )
    calendar_path = schema.TextLine(
            title=_(u'Target calendar path'),
            description=_(
                    u"Enter a folder where the 'next / previous events' "
                    "link will point to. This is optional"),
            required=False,
            )
    rss_path = schema.TextLine(
            title=_(u'RSS path'),
            description=_(
                    u'Enter a relative path to the calendar or topic that '
                    'displays an RSS representation of these events. "/RSS" '
                    'will automatically be appended to the URL. This setting '
                    'is optional'),
            required=False,
            )
    rss_explanation_path = schema.TextLine(
            title=_(u'RSS explanation path'),
            description=_(
                    u'Enter a relative path to a page that gives general RSS '
                    'information. This setting is optional.'),
            required=False,
            )

class Assignment(base.Assignment):
    implements(IEventsPortlet)

    def __init__(self,
                count=5,
                state=('published', ),
                subject=tuple(),
                calendar_path=None,
                rss_path='',
                rss_explanation_path=''):
        self.count = count
        self.state = state
        self.subject = subject
        self.calendar_path = calendar_path
        self.rss_path = rss_path
        self.rss_explanation_path = rss_explanation_path

    @property
    def title(self):
        return _(u"OSH Events")


class Renderer(events.Renderer):
    """Dynamically override standard header for news portlet"""

    _template = ViewPageTemplateFile('oshevents.pt')

    def __init__(self, *args):
        events.Renderer.__init__(self, *args)
        portal_languages = getToolByName(self.context, 'portal_languages')
        self.preflang = portal_languages.getPreferredLanguage()

        portal_state = getMultiAdapter(
                            (self.context, self.request),
                            name=u'plone_portal_state'
                            )
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
        portal_languages = getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()
        calendar_path = self.data.calendar_path
        subject = self.data.subject
        navigation_root_path = self.navigation_root_path
        # http or https?
        server_url = self.request.get('SERVER_URL', '')
        protocol, domain = server_url.split("://")
        return (calendar_path, preflang, subject, navigation_root_path, protocol, domain)

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    # Add respect to INavigationRoot
    @memoize
    def _data(self):
        context = Acquisition.aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_languages = getToolByName(context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()

        # search in the navigation root of the currently selected
        # language and in the canonical path
        # with Language = preferredLanguage or neutral
        current_path = self.context.getPhysicalPath()
        if len(current_path) > 3 and current_path[3] in ('sub', 'fop'):
            # in a subsite, take only the subsite or fop site
            path = '/'.join(self.navigation_root_path.split('/')[:-1])
        else:
            # in the main site, exclude sub
            path = "/osha/portal AND -/osha/portal/sub AND -/osha/portal/fop"

        oshaview = getMultiAdapter((context, self.request),
            name=u'oshaview')
        subsite = oshaview.getCurrentSubsite()
        # calendar = self.getCalendar(preflang)
        # # If we're in the root (i.e. no in a subiste), and a valid pointer to a
        # # calendar exists, use its path as a query parameter
        # if subsite is None and calendar:
        #     paths = ['/'.join(calendar.getPhysicalPath())]

        subject = list(self.data.subject)
        limit = self.data.count

        # make sure to exclude the subs
        query = 'portal_type:(Event) AND ' \
            'review_state:(%(review_state)s) AND path_parents:(%(path)s) ' \
            'AND end:[%(now)s TO *]' % \
                {'review_state': ' OR '.join(self.data.state),
                'path': path,
                'now': iso8601date(DateTime()), }

        # If a subject is selected, use that for the query
        if subject:
            query += ' AND Subject:(%s)' % ' OR '.join(subject)

        lf_search_view = self.context.restrictedTraverse("@@language-fallback-search")
        results = lf_search_view.search_solr(
            query, sort='start asc', rows=limit, lang_query=False)

        return results

    def _render_cachekey_calendar(method, self, preflang):
        calendar_path = self.data.calendar_path
        subject = self.data.subject
        navigation_root_path = self.navigation_root_path
        return (calendar_path, preflang, subject, navigation_root_path)

    @ram.cache(_render_cachekey_calendar)
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
        # if not ICalendarEnhanced.providedBy(cal):
        #     cal = None
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
        osha_view = getMultiAdapter((self.context, self.request), name=u'oshaview')
        show_previous_events = osha_view.get_subsite_property('show_previous_events')
        if show_previous_events is None: #Property does not yet exist. Old
                                         #behaviour was to show previous_events
            show_previous_events = True

        if show_previous_events:
            cal = self.getCalendar(self.preflang)
            if cal is None:
                return ''
            return '%s/past_events.html' % cal.absolute_url()
        return ''

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
        return Assignment(
                    count=data.get('count', 5),
                    state=data.get('state', ('published',)),
                    subject=data.get('subject', tuple()),
                    calendar_path=data.get('calendar_path', None),
                    rss_path=data.get('rss_path',''),
                    rss_explanation_path=data.get('rss_explanation_path','')
                    )


class EditForm(base.EditForm):
    form_fields = form.Fields(IEventsPortlet)
    label = _(u"Edit Events Portlet")
    description = _(u"This portlet lists upcoming Events.")


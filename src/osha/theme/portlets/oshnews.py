from Acquisition import aq_parent, aq_inner
from DateTime import DateTime
from collective.solr.mangler import iso8601date
from osha.theme.browser.utils import search_solr
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.app.portlets.interfaces import IPortletPermissionChecker
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.utils import isExpired
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from types import UnicodeType
from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements


class INewsPortlet(IPortletDataProvider):

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
    newsfolder_path = schema.TextLine(
        title=_(u'Newsfolder path'),
        description=(
            u"Enter a folder where the 'more news' link will "
            "point to. This is optional. If you add a %s, "
            "it will be replaced by the current language."
        ),
        required=False,
    )
    rss_path = schema.TextLine(
        title=_(u'RSS path'),
        description=_(
            u'Enter a relative path to the folder or topic that '
            'displays an RSS representation of the news. '
            '"/RSS" will automatically be appended to the URL.'
            'This setting is optional'
        ),
        required=False,
    )
    rss_explanation_path = schema.TextLine(
        title=_(u'RSS explanation path'),
        description=_(
            u'Enter a relative path to a page that gives '
            'general RSS information. This is optional.'
        ),
        required=False,
    )


class Assignment(base.Assignment):
    implements(INewsPortlet)

    def __init__(
        self, count=5, state=('published', ), subject=tuple(),
        newsfolder_path='', rss_path='', rss_explanation_path=''
    ):

        self.count = count
        self.state = state
        self.subject = subject
        self.newsfolder_path = newsfolder_path
        self.rss_path = rss_path
        self.rss_explanation_path = rss_explanation_path

    @property
    def title(self):
        return _(u"OSH News")


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('oshnews.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_lang = getToolByName(self.context, 'portal_languages')
        self.preflang = portal_lang.getPreferredLanguage()

        portal_state = getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state'
        )

        self.navigation_root_path = portal_state.navigation_root_path()
        portal = portal_state.portal()
        self.root = portal.restrictedTraverse(self.navigation_root_path)

        # backwards compatibility
        if not hasattr(self.data, 'newsfolder_path'):
            self.data.newsfolder_path = ''
        if not hasattr(self.data, 'rss_path'):
            self.data.rss_path = ''
        if not hasattr(self.data, 'rss_explanation_path'):
            self.data.rss_explanation_path = ''
        if not hasattr(self.data, 'subject'):
            self.data.subject = tuple()

    def published_news_items(self):
        return self._data()

    def _render_cachekey(method, self):
        portal_languages = getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()
        newsfolder_path = self.data.newsfolder_path
        subject = self.data.subject
        navigation_root_path = self.navigation_root_path
        return (newsfolder_path, preflang, subject, navigation_root_path)

    @ram.cache(_render_cachekey)
    def available(self):
        return len(self._data())

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def _data(self):
        """Search for news everywhere, then try to find translations in the
        current language. If no translation is found, use the 'en' version.
        """
        current_path = self.context.getPhysicalPath()
        if len(current_path) > 3 and current_path[3] in ('sub', 'fop'):
            # in a subsite, take only the subsite or fop site
            path = '/'.join(self.navigation_root_path.split('/')[:-1])
            INFOP = True
        else:
            # in the main site, exclude sub
            path = "/osha/portal AND -/osha/portal/sub AND -/osha/portal/fop"
            INFOP = False

        subject = list(self.data.subject)
        limit = self.data.count

        # make sure to exclude the subs
        query = '(portal_type:"News Item" OR isNews:true) AND ' \
            'review_state:(%(review_state)s) AND path_parents:(%(path)s) ' \
            'AND effective:[* TO %(effective)s]' % \
            {'review_state': ' OR '.join(self.data.state),
             'path': path,
             'effective': iso8601date(DateTime()), }

        if subject:
            query += ' AND Subject:(%s)' % ' OR '.join(subject)

        if INFOP:
            results = search_solr(query, sort='Date desc', rows=limit)
        else:
            lf_search_view = self.context.restrictedTraverse(
                "@@language-fallback-search")
            results = lf_search_view.search_solr(
                query, sort='Date desc', rows=limit)  # lang_query=False)
        items = list()
        for res in results[:limit]:
            if isExpired(res) and getattr(res, 'outdated', False):
                continue
            try:
                items.append(res.getObject())
            except Exception:
                pass
        return items

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

    @memoize
    def all_news_link(self):
        context = aq_inner(self.context)
        if getattr(self.data, 'newsfolder_path', None):
            newsfolder_path = self.data.newsfolder_path
            if "%s" in newsfolder_path:
                newsfolder_path = newsfolder_path % self.preflang

            if newsfolder_path.startswith('/'):
                newsfolder_path = newsfolder_path[1:]
            if isinstance(newsfolder_path, UnicodeType):
                newsfolder_path = newsfolder_path.encode('utf-8')
            target = self.root.restrictedTraverse(
                newsfolder_path, default=None)
            if target is None:
                # try the canonical
                canroot = self.root.getCanonical()
                target = canroot.restrictedTraverse(
                    newsfolder_path, default=None)
            if target:
                return target.absolute_url()
            else:
                return None

        if not context.isPrincipiaFolderish:
            context = aq_parent(context)

        return '%s/oshnews-view' % context.absolute_url()


class AddForm(base.AddForm):
    form_fields = form.Fields(INewsPortlet)
    label = _(u"Add News Portlet")
    description = _(u"This portlet displays recent News Items.")

    def __call__(self):
        context = aq_parent(aq_parent(aq_inner(self.context)))
        oshaview = getMultiAdapter(
            (context, self.request),
            name=u'oshaview'
        )
        sep = oshaview.getCurrentSingleEntryPoint()
        if sep is not None:
            AddForm.form_fields.get('subject').field.default = sep.Subject()

        IPortletPermissionChecker(aq_parent(aq_inner(self.context)))()
        return super(AddForm, self).__call__()

    def create(self, data):
        return Assignment(
            count=data.get('count', 5),
            state=data.get('state', ('published',)),
            subject=data.get('subject', tuple()),
            newsfolder_path=data.get('newsfolder_path', ''),
            rss_path=data.get('rss_path', ''),
            rss_explanation_path=data.get('rss_explanation_path', '')
        )


class EditForm(base.EditForm):
    form_fields = form.Fields(INewsPortlet)
    label = _(u"Edit News Portlet")
    description = _(u"This portlet displays recent News Items.")

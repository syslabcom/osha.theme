from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from Acquisition import aq_parent, aq_inner
from DateTime import DateTime

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from plone.app.portlets.portlets import base
from plone.app.portlets.interfaces import IPortletPermissionChecker

from Products.AdvancedQuery import Or, Eq, And, In, Le
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from types import UnicodeType

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
            description=_(
                    u"Enter a folder where the 'more news' link will "
                    "point to. This is optional"
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

    def __init__(self, 
                count=5, 
                state=('published', ), 
                subject=tuple(), 
                newsfolder_path='', 
                rss_path='', 
                rss_explanation_path=''):

        self.count = count
        self.state = state
        self.subject = subject
        self.newsfolder_path = newsfolder_path
        self.rss_path = rss_path
        self.rss_explanation_path = rss_explanation_path

    @property
    def title(self):
        return _(u"News")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('oshnews.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

        portal_lang= getToolByName(self.context, 'portal_languages')
        self.preflang = portal_lang.getPreferredLanguage()

        portal_state = getMultiAdapter(
                        (self.context, self.request), 
                        name=u'plone_portal_state')

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

    @property
    def available(self):
        return len(self._data())

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
    def render(self):
        return xhtml_compress(self._template()) 

    @memoize
    def _data(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        if hasattr(catalog, 'getZCatalog'):
            catalog = catalog.getZCatalog()

        # search in the navigation root of the currently selected 
        # language and in the canonical path
        # with Language = preferredLanguage or neutral
        paths = list()
        paths.append(self.navigation_root_path)
        try:
            canonical_path = '/'.join(self.root.getCanonical().getPhysicalPath())
            paths.append(canonical_path)
        except:
            pass
        
        queryA = Eq('portal_type', 'News Item')
        queryB = Eq('isNews', True)
        queryAll = In('review_state', self.data.state) & \
                    In('path', paths) & \
                    In('Language', ['', self.preflang])

        subject = list(self.data.subject)
        if subject:
            queryAll = queryAll & In('Subject', subject)

        queryEffective = Le('effective', DateTime())

        query = And(Or(queryA, queryB), queryAll, queryEffective)

        limit = self.data.count
        return catalog.evalAdvancedQuery(query, (('Date', 'desc'),) )[:limit]

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
            if newsfolder_path.startswith('/'):
                newsfolder_path = newsfolder_path[1:]
            if isinstance(newsfolder_path, UnicodeType):
                newsfolder_path = newsfolder_path.encode('utf-8')
            target = self.root.restrictedTraverse(newsfolder_path, default=None)
            if target is None:
                # try the canonical
                canroot = self.root.getCanonical()
                target = canroot.restrictedTraverse(newsfolder_path, default=None)
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
                    rss_explanation_path=data.get('rss_explanation_path','')
                    )


class EditForm(base.EditForm):
    form_fields = form.Fields(INewsPortlet)
    label = _(u"Edit News Portlet")
    description = _(u"This portlet displays recent News Items.")



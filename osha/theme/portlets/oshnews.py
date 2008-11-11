from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.cache import render_cachekey

from Acquisition import aq_inner, aq_parent
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget
from Products.AdvancedQuery import Or, Eq, And, In, Le
from DateTime import DateTime

class INewsPortlet(IPortletDataProvider):

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
    target_newsfolder = schema.Choice(title=_(u"Target newsfolder"),
                                  description=_(u"Select a folder where the 'more news' link will point to. This is optional"),
                                  required=False,
                                  source=SearchableTextSourceBinder({},
                                                                    default_query='path:'))

    rss_path = schema.TextLine(title=_(u'RSS path'),
                               description=_(u'Enter a relative path to the URL that displays an RSS representation of these news. This is optionaö'),
                               required=False,
                               )
    rss_explanation_path = schema.TextLine(title=_(u'RSS explanation path'),
                               description=_(u'Enter a relative path to a page that gives general RSS information. This is optional.'),
                               required=False,
                               )

class Assignment(base.Assignment):
    implements(INewsPortlet)

    def __init__(self, count=5, state=('published', ), target_newsfolder=None, rss_path='', rss_explanation_path=''):
        self.count = count
        self.state = state
        self.target_newsfolder = target_newsfolder
        self.rss_path = rss_path
        self.rss_explanation_path = rss_explanation_path

    @property
    def title(self):
        return _(u"News")

class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('oshnews.pt')

    @property
    def available(self):
        return len(self._data())

    def published_news_items(self):
        return self._data()

#    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template()) 

#    @memoize
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
        return catalog.evalAdvancedQuery(query, (('Date', 'desc'),) )[:limit]

    def showRSS(self):
        return bool(self.data.rss_path)

    def getRSSLink(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        return navigation_root_path + self.data.rss_path

    def getRSSExplanationLink(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        return navigation_root_path + self.data.rss_explanation_path


#    @memoize
    def all_news_link(self):
        
        if self.data.target_newsfolder:
            return self.data.target_newsfolder

        context = aq_inner(self.context)
        if not context.isPrincipiaFolderish:
            context = aq_parent(context)
        
        return '%s/oshnews-view' % context.absolute_url()

class AddForm(base.AddForm):
    form_fields = form.Fields(INewsPortlet)
    form_fields['target_newsfolder'].custom_widget = UberSelectionWidget
    label = _(u"Add News Portlet")
    description = _(u"This portlet displays recent News Items.")

    def create(self, data):
        return Assignment(count=data.get('count', 5), state=data.get('state', ('published',)))

class EditForm(base.EditForm):
    form_fields = form.Fields(INewsPortlet)
    form_fields['target_newsfolder'].custom_widget = UberSelectionWidget
    label = _(u"Edit News Portlet")
    description = _(u"This portlet displays recent News Items.")

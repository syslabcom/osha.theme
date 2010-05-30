from zope.interface import implements
import Acquisition
from plone.portlet.collection import collection
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.app.portlets.cache import get_language
from types import UnicodeType

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
from zope.formlib import form

from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from osha.theme.browser.uberselectionwidget import UberSelectionWidget

from Products.ATContentTypes.interface import IATTopic

from plone.portlet.collection import PloneMessageFactory as _

class ICollectionPortlet(IPortletDataProvider):
    """A portlet which renders the results of a collection object.
    """

    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)

    target_collection = schema.Choice(title=_(u"Target collection"),
                                  description=_(u"Find the collection which provides the items to list"),
                                  required=True,
                                  source=SearchableTextSourceBinder({'object_provides' : IATTopic.__identifier__},
                                                                    default_query='path:'))

    limit = schema.Int(title=_(u"Limit"),
                       description=_(u"Specify the maximum number of items to show in the portlet. "
                                       "Leave this blank to show all items."),
                       required=False)

    show_more = schema.Choice(title=_(u"Show more... link"),
                       description=_(u"If enabled, a more... link will appear in the footer of the portlet. "
                                    "You can determine if it should link to the underlying Collection or show "
                                    "the Collection's contents in the current context."),
                       required=False,
                       vocabulary=SimpleVocabulary(terms=(SimpleTerm(value='',title='No'),
                               SimpleTerm(value='direct', title='Link to collection'),
                               SimpleTerm(value='context', title='Show contents in context')),
                              ),
                       default=''
                       )

    show_dates = schema.Bool(title=_(u"Show dates"),
                       description=_(u"If enabled, effective dates will be shown underneath the items listed."),
                       required=True,
                       default=False)

    show_rss = schema.Bool(title=_(u'Show RSS link'),
                               description=_(u'If enabled, a link to the RSS representaion of the collection will we added at the bottom of the portlet.'),
                               required=True,
                               default=False,
                               )

    rss_explanation_path = schema.TextLine(title=_(u'RSS explanation path'),
                               description=_(u'Enter a relative path to a page that gives general RSS information. This is optional.'),
                               required=False,
                               )

def render_cachekey(fun, self):
    """
    Generates a key based on:

    * Portal URL
    * Negotiated language
    * Anonymous user flag
    * Portlet manager
    * Assignment
    * URL of collection used (instead of using _data)
    
    """
    context = Acquisition.aq_inner(self.context)

    fingerprint = self.collection_url()
    anonymous = getToolByName(context, 'portal_membership').isAnonymousUser()

    key= "".join((
        getToolByName(Acquisition.aq_inner(self.context), 'portal_url')(),
        get_language(Acquisition.aq_inner(self.context), self.request),
        str(anonymous),
        self.manager.__name__,
        self.data.__name__,
        fingerprint))
    return key

class Assignment(collection.Assignment):
    """
    Portlet assignment.    
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(ICollectionPortlet)

    header = u""
    target_collection=None
    limit = None
    show_more = 'direct'
    show_dates = False
    show_rss = False
    rss_explanation_path = ''

    def __init__(self, header=u"", target_collection=None, limit=None, show_more=True, show_dates=False, show_rss=False, rss_explanation_path=''):
        self.header = header
        self.target_collection = target_collection
        self.limit = limit
        self.show_more = show_more
        self.show_dates = show_dates
        self.show_rss = show_rss
        self.rss_explanation_path = rss_explanation_path


class Renderer(collection.Renderer):
    """Portlet renderer.
    
    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """    
    _template = ViewPageTemplateFile('collection.pt')


    def __init__(self, *args):
        collection.Renderer.__init__(self, *args)

        portal_languages = getToolByName(self.context, 'portal_languages')
        self.preflang = portal_languages.getPreferredLanguage()

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        self.navigation_root_path = portal_state.navigation_root_path()
        portal = portal_state.portal()
        self.root = portal.restrictedTraverse(self.navigation_root_path)

    @ram.cache(render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @memoize
    def collection_url(self):
        collection = self.collection()
        if collection is None:
            return None

        if self.data.show_more == 'direct':
            return collection.absolute_url()

        else:
            collectionpath = "/".join(collection.getPhysicalPath())
            
            context = Acquisition.aq_inner(self.context)
            if not context.isPrincipiaFolderish:
                context = Acquisition.aq_parent(context)
            contextpath = "/".join(context.getPhysicalPath())
            return "%s/@@oshtopic-view?tp=%s" % (context.absolute_url(), collectionpath)

#    @memoize
    def getPath(self, ob):
        path = ob.getURL()
        context = Acquisition.aq_inner(self.context)
        portal_properties = getToolByName(context, 'portal_properties')
        viewtypes = portal_properties.site_properties.getProperty('typesUseViewActionInListings')
        if ob.portal_type in viewtypes:
            path = path+'/view'
        return path


    def showRSS(self):
        return bool(self.data.show_rss)

    def getRSSLink(self):
        return '%s/RSS' % self.collection_url()

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
    """Portlet add form.
    
    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(ICollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    
    label = _(u"Add Collection Portlet")
    description = _(u"This portlet display a listing of items from a Collection.")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.
    
    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(ICollectionPortlet)
    form_fields['target_collection'].custom_widget = UberSelectionWidget

    label = _(u"Edit Collection Portlet")
    description = _(u"This portlet display a listing of items from a Collection.")
 

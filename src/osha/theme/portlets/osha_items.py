from Acquisition import aq_inner

from zope import schema
from zope.interface import implements
from zope.formlib import form
from zope.i18n import translate
from zope.app.component.hooks import getSite

from plone.app.portlets.portlets import base
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from Products.Archetypes.utils import shasattr
from Products.ATContentTypes.interface import folder
from Products.ATContentTypes.interface import document
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from slc.seminarportal.portlets.base import BaseRenderer
from osha.theme import OSHAMessageFactory as _

class IOSHAItemsPortlet(IPortletDataProvider):
    """ """
    header = schema.TextLine(
                    title=_(u"Portlet header"),
                    description=_(u"The display title of the rendered portlet"),
                    required=True
                    )
    count = schema.Int(
                    title=_(u'Number of items to display'),
                    required=True,
                    default=3
                    )
    types = schema.Tuple(title=_(u"Content Type"),
                    description=_(
                            u"Please specify the content types of the items "
                            u"to be displayed in this portlet."),
                    required=True,
                    value_type=schema.Choice(
                        vocabulary="osha.theme.FriendlyTypesVocabulary"),
                    )
    state = schema.Tuple(title=_(u"Workflow state"),
                    description=_(
                            u"You may limit the displayed items to a "
                            u"specific workflow state. By default all "
                            u"published items will be shown."),
                    default=('published',),
                    required=True,
                    value_type=schema.Choice(
                        vocabulary="plone.app.vocabularies.WorkflowStates")
                    )
    subject = schema.Tuple(
                    title=_(u"Categories"),
                    description=_(
                            u"Pick one or more categories with which you want "
                            u"to filter the items shown in this portlet."),
                    default=tuple(),
                    value_type=schema.Choice(
                        vocabulary="osha.theme.SubjectValuesVocabulary"),
                    )
    sort = schema.Choice(
                    title=_(u"Sorting Criterion"),
                    description=_(
                            u"Please choose the criterion on which the items "
                            u"should be sorted."),
                    default='effective',
                    vocabulary="osha.theme.SortableIndexesVocabulary",
                    )
    portletlink = schema.Choice(
                    title=_(u'Portlet link'),
                    description=_(
                            u"Choose a folder or page to which this portlet's "
                            u"title and the bottom link will point to. This "
                            u"is optional."
                            ),
                    required=False,
                    source=SearchableTextSourceBinder(
                        {'object_provides': [
                                        folder.IATFolder.__identifier__,
                                        folder.IATBTreeFolder.__identifier__,
                                        document.IATDocument.__identifier__,
                                        ]},
                        default_query='path:'),
                    )

class Renderer(BaseRenderer):
    """ """
    _template = ViewPageTemplateFile('osha_items.pt')

    def _render_cachekey(method, self):
        portal_languages = getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()
        subject = self.data.subject
        navigation_root_path = self.navigation_root_path
        return (preflang, subject, navigation_root_path)

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    @property
    def title(self):
        portal_languages = getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()
        return translate(
                    msgid=self.data.header, 
                    domain='osha',
                    target_language=preflang, 
                    context=self.context
                    ) 

    def portlet_link(self):
        """ The portlet will not appear if there aren't any items to display.
        """
        if self.data.portletlink:
            portal = getSite()
            return "%s/%s"  % (getSite().absolute_url(), self.data.portletlink)

    @property
    def available(self):
        """ The portlet will not appear if there aren't any items to display.
        """
        return len(self.items()) > 0

    @memoize
    def items(self):
        return self._data()

    def _data(self):
        """ Get all items that conform to the workflow state and
            category specified on the portlet.
        """
        if self.data.count == 0:
            return []

        context = aq_inner(self.context)
        # search in the navigation root of the currently selected language 
        paths = [self.navigation_root_path]
        if self.navigation_root:
            # Also search in its canonical
            if shasattr(self.navigation_root, 'getCanonical'):
                canonical = self.navigation_root.getCanonical()
                if canonical is not None:
                    paths.append('/'.join(canonical.getPhysicalPath()))

        # Search: Language = preferredLanguage or neutral
        preflang = getToolByName(context, 'portal_languages').getPreferredLanguage()
        query = dict(
                    Language=['', preflang],
                    path=paths,
                    portal_type=self.data.types,
                    review_state=self.data.state,
                    sort_limit=self.data.count,
                    limit=self.data.count,
                    sort_on=self.data.sort or 'created',
                    sort_order='reverse',
                    )

        if self.data.subject:
            if type(self.data.subject) in [str, unicode]:
                query.update(Subject=(self.data.subject,))
            else:    
                query.update(Subject=self.data.subject)

        catalog = getToolByName(context, 'portal_catalog')
        return catalog.searchResults(**query)


class Assignment(base.Assignment):
    implements(IOSHAItemsPortlet)

    def __init__(       
                self, 
                count=5, 
                header=None,
                portletlink=None,
                sort=None,
                state=('published', ), 
                subject=tuple(), 
                types=None,):

        self.count = count
        self.header = header
        self.portletlink = portletlink
        self.sort = sort
        self.state = state
        self.subject = subject
        self.types = types

    @property
    def title(self):
        return self.header


class AddForm(base.AddForm):
    form_fields = form.Fields(IOSHAItemsPortlet)
    label = _(u"Adding the OSHA Items Portlet")
    description = _(
        u"This portlet lists items of a specific type, filtered by category.")
        
    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IOSHAItemsPortlet)
    label = _(u"Editing the OSHA Items Portlet")
    description = _(
        u"This portlet lists items of a specific type, filtered by category.")


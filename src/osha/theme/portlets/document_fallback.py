import Acquisition, re
from zope.interface import implements
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form

from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.memoize.compress import xhtml_compress

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from Products.ATContentTypes.interface import IATDocument
from Products.CMFCore.utils import getToolByName

from osha.theme import OSHAMessageFactory as _
from plone.portlet.collection import PloneMessageFactory as _plone

IDS_FOR_TRACKING = ['top5']

class IDocumentFallbackPortlet(IPortletDataProvider):
    """A portlet which renders the contents of a Document object and
    provides fallback to the canonical object.
    """

    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)

    target_document = schema.Choice(
        title=_(u"Target document"),
        description=_(u"Find the document which provides the content"),
        required=True,
        source=SearchableTextSourceBinder(
            {'object_provides' : IATDocument.__identifier__},
            default_query='path:'))

    omit_border = schema.Bool(
        title=_(u"Omit portlet border"),
        description=_(u"Tick this box if you want to render the text above "
                      "without the standard header, border or footer."),
        required=True,
        default=False)

class Assignment(base.Assignment):
    """
    Portlet assignment.
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IDocumentFallbackPortlet)

    header = u""
    target_document=None
    omit_border = False

    def __init__(self, header=u"", target_document=None, omit_border=False):
        self.header = header
        self.target_document = target_document
        self.omit_border = omit_border

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen. Here, we use the title that the user gave.
        """
        return self.header


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    _template = ViewPageTemplateFile('document_fallback.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = Acquisition.aq_base(self.context)
        portal_languages = getToolByName(self.context, 'portal_languages')
        self.preflang = portal_languages.getPreferredLanguage()
        self.myid = self.data.target_document.split('/')[-1]

    def _render_cachekey(method, self):
        preflang = getToolByName(
            self.context, 'portal_languages').getPreferredLanguage()
        portal_membership = getToolByName(self.context, 'portal_membership')
        member = portal_membership.getAuthenticatedMember()
        roles = member.getRolesInContext(self.context)
        modified = self.document() and self.document().modified() or ''
        return (modified, roles, preflang)

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())


    def title(self):
        f = self.fallback(self.preflang)
        if f is None:
            return ''
        title = f.Title()
        if type(title)!=type(u''):
            try: title = unicode(title, 'utf-8')
            except: pass
        return _(title)

    @memoize
    def editable(self):
        f = self.fallback(self.preflang)
        if f is None:
            return False
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.checkPermission('Modify portal content', f)

    @memoize
    def editlink(self):
        f = self.fallback(self.preflang)
        if f is None:
            return ''
        return f.absolute_url()+'/edit'

    @memoize
    def content(self):
        f = self.fallback(self.preflang)
        if f is None:
            return ''
        text = f.getText()
        if self.myid in IDS_FOR_TRACKING:
            text = self.modifyLinks(text)
        return text


    @memoize
    def fallback(self, preflang):
        doc = self.document()
        if doc is None:
            return None
        pref = doc.getTranslation(preflang)
        if not pref:
            canonical = doc.getCanonical()
            return canonical
        return pref


    def replace_link(self, mobj):
        link = mobj.group(1)
        if '?' in link:
            text = mobj.group(0).replace(
                link, '%s&sourceid=%s' %(link, self.myid))
        else:
            text = mobj.group(0).replace(
                link, '%s?sourceid=%s' %(link, self.myid))
        return text

    def modifyLinks(self, text):
        """ Append ?sourceid=document's id to all links """
        pattstr = "\<a.*?href=[\"'](.*?)[\"']"
        patt = re.compile(pattstr, re.I|re.S)
        mobj = patt.search(text)
        if mobj:
            text = patt.sub(self.replace_link, text)
        return text

    @memoize
    def document(self):
        """ get the document the portlet is pointing to
            fall back to the canonical if language version cannot be found
        """
        document_path = self.data.target_document
        if not document_path:
            return None

        if document_path.startswith('/'):
            document_path = document_path[1:]

        if not document_path:
            return None

        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        portal = portal_state.portal()
        return portal.restrictedTraverse(document_path, default=None)


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IDocumentFallbackPortlet)
    form_fields['target_document'].custom_widget = UberSelectionWidget

    label = _(u"Add Document Fallback Portlet")
    description = _(u"This portlet displays the contents of a document.")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """

    form_fields = form.Fields(IDocumentFallbackPortlet)
    form_fields['target_document'].custom_widget = UberSelectionWidget

    label = _(u"Edit Document Fallback Portlet")
    description = _(u"This portlet displays the contents of a document.")

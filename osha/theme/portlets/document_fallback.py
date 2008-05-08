import Acquisition
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

from plone.portlet.collection import PloneMessageFactory as _

class IDocumentFallbackPortlet(IPortletDataProvider):
    """A portlet which renders the contents of a Document object and provides fallback to the canonical object.
    """

    header = schema.TextLine(title=_(u"Portlet header"),
                             description=_(u"Title of the rendered portlet"),
                             required=True)

    target_document = schema.Choice(title=_(u"Target document"),
                                  description=_(u"Find the document which provides the content"),
                                  required=True,
                                  source=SearchableTextSourceBinder({'object_provides' : IATDocument.__identifier__},
                                                                    default_query='path:'))
                      
class Assignment(base.Assignment):
    """
    Portlet assignment.    
    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IDocumentFallbackPortlet)

    header = u""
    target_document=None

    def __init__(self, header=u"", target_document=None):
        self.header = header
        self.target_document = target_document

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

    # Cached version - needs a proper cache key
    # @ram.cache(render_cachekey)
    # def render(self):
    #     if self.available:
    #         return xhtml_compress(self._template())
    #     else:
    #         return ''

    render = _template

    def title(self):
        f = self.fallback(self.preflang)
        if f is None:
            return ''
        return f.Title() 
       
    def editable(self):
        f = self.fallback(self.preflang)
        if f is None:
            return False
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.checkPermission('Modify portal content', f)
        
    def editlink(self):
        f = self.fallback(self.preflang)
        if f is None:
            return ''
        return f.absolute_url()+'/edit'   

       
    def content(self):
        f = self.fallback(self.preflang)
        if f is None:
            return ''
        return f.getText()


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

        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
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

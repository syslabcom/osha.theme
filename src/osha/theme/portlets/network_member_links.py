from zope.interface import implements
from zope.formlib import form

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone.portlets.interfaces import IPortletDataProvider
from plone.memoize.instance import memoize
from plone.app.portlets.portlets import base

try:
    from osha.adaptation.subtyper import IAnnotatedLinkList
except ImportError:
    from osha.policy.adapter.subtyper import IAnnotatedLinkList

try:
    from osha.adaptation.vocabulary import AnnotatableLinkListVocabulary
except ImportError:
    from osha.theme.vocabulary import AnnotatableLinkListVocabulary

class IOSHNetworkMemberLinksPortlet(IPortletDataProvider):
    pass

class Assignment(base.Assignment):

    implements(IOSHNetworkMemberLinksPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return "Network Member Links"


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('network_member_links.pt')
    link_sections = AnnotatableLinkListVocabulary().getDisplayList()

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        return (preflang)
        
    #@ram.cache(_render_cachekey)
    def render(self):
        return self._template()

    def has_links(self):
        """ Check if this page has been subtyped to provide annotated
        links """
        context = self.context
        return IAnnotatedLinkList.providedBy(context) and \
            context.Schema().getField('annotatedlinklist').get(context)
        
    @memoize
    def get_links_by_section(self, section):
        context = self.context
        if IAnnotatedLinkList.providedBy(self.context):
            links = context.Schema().getField('annotatedlinklist').get(context)
            return [i for i in links if i["section"] == section]
        else:
            return None

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = self.context

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IOSHNetworkMemberLinksPortlet)

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IOSHNetworkMemberLinksPortlet)

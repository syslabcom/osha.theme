from DateTime import DateTime

from zope.app.component.hooks import getSite
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from osha.theme.browser.interfaces import IOSHNetworkMemberView

_ = MessageFactory('osha.theme')

class OSHNetworkMemberView(BrowserView):
    implements(IOSHNetworkMemberView)

    template = ViewPageTemplateFile("templates/oshnetwork_member_view.pt")
    template.id = "oshnetwork-member-view"

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.result = []
        self.request.set('disable_border', True)

    def __call__(self):
        return self.template()

    def getLocalizedPath(self, path):
        """ A method to prefix a path with the currently selected language
        string """
        context = self.context
        language = context.Language()
        # Remove any '/' from the start of the path
        path = path.lstrip("/")
        return "/%s/%s" % (language, path)

    def getNationalFlag(self):
        context = self.context
        country = context.aq_inner.aq_parent.getId()
        flag = country + "_large.gif"
        try:
            img = context.restrictedTraverse(flag)
            flag_tag = img.tag()
        except AttributeError:
            flag_tag = ""

        return flag_tag

    def getNews(self):
        """ return the brains for relevant news items """
        context = self.context
        catalog = getToolByName(context, 'portal_catalog')
        language = context.Language()
        now = DateTime()
        query = dict(portal_type='News Item',
                     review_state='published',
                     effective={'query': now,
                          'range': 'max'},
                     expires={'query': now,
                          'range': 'min'},
                     sort_on='effective',
                     sort_order='reverse',
                     Language=language)

        brains = catalog(query)
        return brains

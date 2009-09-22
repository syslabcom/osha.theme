from DateTime import DateTime

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
        """ Look for an image called 'national_flag.png' in the folder
        of the canonical translation of the network member. """
        context = self.context
        canonical_parent = context.getCanonical().aq_inner.aq_parent
        flag = None
        flag_src = "national_flag.png"
        if flag_src in canonical_parent.objectIds():
            path = canonical_parent.absolute_url_path()
            flag = context.unrestrictedTraverse(path+"/"+flag_src)
        return flag

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

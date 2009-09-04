from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from Products.Five import BrowserView

from osha.theme.browser.interfaces import IOSHNetworkMemberView

_ = MessageFactory('osha.theme')

class OSHNetworkMemberView(BrowserView):
    implements(IOSHNetworkMemberView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.result = []

    def getLocalizedPath(self, path):
        """ A method to prefix a path with the currently selected language
        string """
        context = self.context
        language = context.Language()
        # Remove any '/' from the start of the path
        path = path.lstrip("/")
        return "/%s/%s" % (language, path)


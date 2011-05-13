from zope.i18nmessageid import MessageFactory
from AccessControl import ModuleSecurityInfo

_ = OSHAMessageFactory = MessageFactory('osha')

def initialize(context):
    """Intializer called when used as a Zope 2 product."""
    ModuleSecurityInfo('osha.theme.config').declarePublic('EUROPEAN_NETWORK')

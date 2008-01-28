from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager

from plone.portlets.interfaces import IPortletManager

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """
    
class IOSHAHeaderTopactions(IViewletManager):
    """A viewlet manager that sits in the portal-header and wraps top actions
    """    
    
class IOSHAHeaderDropdowns(IViewletManager):
    """A viewlet manager with top dropdowns, incl. language selector
    """

class IOSHAAboveContent(IPortletManager):
    """Portlet manager above the content area.
    """   
    
class IOSHABelowContent(IPortletManager):
    """Portlet manager below the content area.
    """     

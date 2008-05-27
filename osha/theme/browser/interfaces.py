from zope.interface import Interface
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager

from plone.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IColumn

class IOSHAThemeLayer(Interface):
    """ Marker Interface used by BrowserLayer
    """
    
class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """

class IHW2008Specific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """

class ILinguaToolsView(Interface):
    """ A tool to manage lingua specific tasks """

    def propagatePortlets():
        """ propagates the portlet config from context to the language versions """

    def deleter(id):
        """ deletes an object with a given id from all language branches """

    def fixOrder(ORDER):
        """Move contents of a folter into order
            make sure the ordering of the folders is correct
        """

    def renamer(oldid, newid):
        """ rename one object within context from oldid to newid """
    def setTitle(title):
        """ simply set the title to a given value. Very primitive! """
    def setEnableNextPrevious(flag=True):
        """ Enables the Next-Previous Navigation Flag """
    def setExcludeFromNav(flag=True):
        """ Sets the Exclude From nav flag """
    def setProperty(id, typ, value):
        """ sets a OFS Property on context """
    def delProperty(id):
        """ removes a OFS Property on context """
    def setTranslatedTitle(label, domain):
        """ sets the title based on the translation availble for title in the language """
    def createFolder(id, excludeFromNav=True):
        """ creates a folder and all translations in the language branches """
    def cutAndPaste(self, sourcepath, id, targetpath):
        """ uses OFS to cur and paste an object
            sourecpath must refer to the folder which contains the object to move
            id must be a string containing the id of the object to move
            targetpath must be the folder to move to
            both paths must contain one single %s to place the language
        """
    def addLanguageTool(self):
        """ adds a language Tool """

    def subtyper(subtype):
        """ subtypes object to the given subtype """


class IOSHA(Interface):
    """ A tool view with OSHA specifics """
    
    def cropText(text, length, ellipsis):
        """ Crop text on a word boundary """
        
    def listMetaTags(context):
        """ retrieve the metadata for the header and make osha specific additions """

    def sendto(self, send_to_address, send_from_address, comment,
               subject='Plone', **kwargs):
        """Sends a link of a page to someone."""
    
class IOSHAHeaderTopactions(IViewletManager):
    """A viewlet manager that sits in the portal-header and wraps top actions
    """    
    
class IOSHAHeaderDropdowns(IViewletManager):
    """A viewlet manager with top dropdowns, incl. language selector
    """

class IAdditionalPortletManager(IPortletManager, IColumn):
    """ is a manager and a column """
    
class IOSHAAboveContent(IAdditionalPortletManager):
    """Portlet manager above the content area.
    """   
    
class IOSHABelowContent(IAdditionalPortletManager):
    """Portlet manager below the content area.
    """     

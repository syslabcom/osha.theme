from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.viewlet.interfaces import IViewletManager

from plone.app.portlets.interfaces import IColumn
from plone.theme.interfaces import IDefaultPloneLayer
from plone.portlets.interfaces import IPortletManager

_ = MessageFactory('osha.theme')

class IOSHAThemeLayer(Interface):
    """ Marker Interface used by BrowserLayer
    """
    
class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """

class IHW2008Specific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """

class IGermanySpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """

class IRISQSpecific(IDefaultPloneLayer, IOSHAThemeLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """

class ISafestartSpecific(IDefaultPloneLayer, IOSHAThemeLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """

class INAPOSpecific(IDefaultPloneLayer, IOSHAThemeLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """


class IPressRoomView(Interface):
    """ A View for Pressroom to show Snydication Information """

    def get_syn_news():
        """ A method to get the syndicated News """


class IPressRoomConfiguration(Interface):
    """ This interface defines the configuration form """
    feed_key = schema.List(
                        title=_(u"RSS Feed"),
                        description=_(u"Choose the RSS profile for this PressRoom. Profiles are created in the site control panel."),
                        value_type=schema.Choice(vocabulary="osha.theme.SinToolKeyVocabulary"),
                        required=False) 

    press_contacts = schema.List(
                        title=_(u"Reference to the Press Contacts"),
                        value_type=schema.Choice(vocabulary="osha.theme.PressContactVocabulary"),
                        required=False) 

    keyword_list = schema.TextLine(title=_(u"Filtering Keywords"),
                    description=_(u'Add your keywords here, separate them with spaces.'),
                    required=False)


class IRollingQuotesToolsView(Interface):

    def update():
        """updates rollingquotesportlet"""

class INapoFilmView(Interface):
    """ A ViewClass that renders a View based on a datastructure"""

    def getFilms(self):
        """ returns a list with all informations about all Films"""

    def getTitle(self,filmID):
        """ returns the title of a spezific Film identified by the
            string parameter filmID """

    def getDescription(self,filmID):
        """ returns the description of a spezific Film identified by the
            string parameter filmID"""

    def getDURLAVI(self,filmID):
        """ returns the URL of the FIlm specified by the string parameter FilmID
            in AVI format"""

    def getDURLWMV(self,filmID):
        """ returns the URL of the FIlm spezified by the string parameter FilmID
            in WMV format"""

class INapoEpisodeView(Interface):

    def getEpisodes(self,filmID):
        """ returns all Episodes of a film specified by the string 
            parameter filmID"""

    def getEpisodeTitle(self,filmID,EpisodeNumber):
        """ returns the title of a specific Episode, selected by the 
            Parameters FilmID which selects the Film, and the int
            Episodnumber"""

    def getEpisodeImage(self,filmID,EpisodeNumber):
        """ returns the URL of an Preview Image of an Episode selected
            by the string parameter filmID and the int parameter
            EpisodeNumber"""

    def getEpisodeDURLAVI(self,filmID,EpisodeNumber):
        """ returns the URL of the Episode in AVI Format selected
            by the string parameter filmID and the int parameter
            EpisodeNumber"""

    def getEpisodeDURLWMV(self,filmID,EpisodeNumber):
        """ returns the URL of the Episode in WMV Format selected
            by the string parameter filmID and the int parameter
            EpisodeNumber"""

class IOSHA(Interface):
    """ A tool view with OSHA specifics """
    
    def cropHtmlText(text, length, ellipsis):
        """ Crop text on a word boundary """
        
    def listMetaTags(context):
        """ retrieve the metadata for the header and make osha specific additions """

    def sendto(self, send_to_address, send_from_address, comment,
               subject='Plone', **kwargs):
        """Sends a link of a page to someone."""

    def getTranslatedCategories(domain):
        """ returns a list of tuples, that contain key and title of Categories (Subject)
        ordered by Title """

    def getCurrentSingleEntryPoint():
        """ returns the SEP in the current path if we are inside one. None otherwise """

    def getSingleEntryPoints():
        """ Retrieve all sections implementing ISubsite that match the local Subjects """

    def getSingleEntryPointsBySubject(subjects):
        """ Retrieve all sections implementing ISubsite that match the local Subjects """

    def getGermanNetwork():
        """ returns the sites from the European Network """
        
    def getEuropeanNetwork():
        """ returns the sites from the European Network """
    
    def getInternationalNetwork():
        """ returns the sites from the European Network """

    def makeAbsoluteUrls(text):
        """ make absolute urls out of relative urls """

    def subsiteRootUrl():
        """ return URL of subsite """

    def subsiteRootPath():
        """ return path of subsite """

    def get_subsite_property(name):
        """ return the prop with name from the subsite """

    def set_subsite_property(name, value):
        """ Set a prop with the name to value on the subsite """

    def getCalendarEvents(start, stop, reverse):
        """ If called on a calendar, the list of events is returned"""
    
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

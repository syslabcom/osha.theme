from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from zope.viewlet.interfaces import IViewletManager

from plone.app.portlets.interfaces import IColumn
from plone.theme.interfaces import IDefaultPloneLayer
from plone.portlets.interfaces import IPortletManager

_ = MessageFactory('osha.theme')

class IMaintenanceView(Interface):
    "Maintenance Plone4"

    def convertLPFolders():
        """ convert Large Plone Folders to Folders """

class IOSHmailView(Interface):
    """ oshmail overview including subscription """

    def subscribe():
        """ subscribe to oshmail """

class IFullWidth(Interface):
    """Marker Interface to indicate that the right slot should be made
    available to the content area as well.
    """

class IOSHAThemeLayer(Interface):
    """ Marker Interface used by BrowserLayer
    """

class IThemeSpecific(IDefaultPloneLayer, IOSHAThemeLayer):
    """Marker interface that defines a Zope 3 skin layer.
    """

class IHW2008Specific(IThemeSpecific):
    """Marker interface that defines a Zope 3 skin layer.
    """

class IGermanySpecific(IThemeSpecific):
    """Marker interface that defines a Zope 3 skin layer.
    """

class IRISQSpecific(IThemeSpecific):
    """Marker interface that defines a Zope 3 skin layer.
    """

class ISafestartSpecific(IThemeSpecific):
    """Marker interface that defines a Zope 3 skin layer.
    """

class INAPOSpecific(IThemeSpecific):
    """Marker interface that defines a Zope 3 skin layer.
    """

class IPressRoomView(Interface):
    """ A View for Pressroom to show Snydication Information """

    def getFeed():
        """A method to get the syndicated News.

        XXX: Deprecated, use getRSSFeed instead
        """

    def getRSSFeed():
        """A method to get the syndicated news about OSHA"""

    def getPresscontacts():
        """Return relevant data for the 3 press contacts (international,
        Spanish, Brussels)
        """

class IPressRoomConfiguration(Interface):
    """ This interface defines the configuration form """
    feed_key = schema.List(
        title=_(u"RSS Feed"),
        description=_(u"Choose the RSS profile for this PressRoom. Profiles \
                      are created in the site control panel."),
        value_type=schema.Choice(
            vocabulary="osha.theme.SinToolKeyVocabulary"),
        required=False
    )

    press_contacts = schema.List(
        title=_(u"Reference to the Press Contacts"),
        value_type=schema.Choice(
            vocabulary="osha.theme.PressContactVocabulary"),
        required=False
    )

    keyword_list = schema.TextLine(
        title=_(u"Filtering Keywords"),
        description=_(u'Add your keywords here, separate them with spaces.'),
        required=False
    )


class IRollingQuotesToolsView(Interface):

    def update():
        """updates rollingquotesportlet"""

class INapoFilmView(Interface):
    """A ViewClass that renders a View based on a datastructure"""

    def getFilms(self):
        """Return a list with all informations about all Films"""

    def getTitle(self, filmID):
        """Return the title of a spezific Film identified by the
        string parameter filmID.
        """

    def getDescription(self, filmID):
        """Return the description of a spezific Film identified by the
        string parameter filmID.
        """

    def getDURLAVI(self, filmID):
        """Return the URL of the FIlm specified by the string parameter
        FilmID in AVI format.
        """

    def getDURLWMV(self, filmID):
        """Return the URL of the FIlm specified by the string parameter
        FilmID in WMV format.
        """

class INapoEpisodeView(Interface):

    def getEpisodes(self, filmID):
        """ returns all Episodes of a film specified by the string
        parameter filmID.
        """

    def getEpisodeTitle(self, filmID, EpisodeNumber):
        """ returns the title of a specific Episode, selected by the
        Parameters FilmID which selects the Film, and the int
        Episodnumber.
        """

    def getEpisodeImage(self, filmID, EpisodeNumber):
        """ returns the URL of an Preview Image of an Episode selected
        by the string parameter filmID and the int parameter
        EpisodeNumber.
        """

    def getEpisodeDURLAVI(self, filmID, EpisodeNumber):
        """ returns the URL of the Episode in AVI Format selected
        by the string parameter filmID and the int parameter
        EpisodeNumber.
        """

    def getEpisodeDURLWMV(self, filmID, EpisodeNumber):
        """ returns the URL of the Episode in WMV Format selected
        by the string parameter filmID and the int parameter
        EpisodeNumber.
        """

class IOSHA(Interface):
    """ A tool view with OSHA specifics """

    def cropHtmlText(text, length, ellipsis):
        """ Crop text on a word boundary """

    def listMetaTags(context):
        """ retrieve the metadata for the header and make osha specific
        additions.
        """

    def sendto(self, send_to_address, send_from_address, comment,
               subject='Plone', **kwargs):
        """Sends a link of a page to someone."""

    def getTranslatedCategories(domain):
        """ returns a list of tuples, that contain key and title of
        Categories (Subject) ordered by Title.
        """

    def getCurrentSingleEntryPoint():
        """ returns the SEP in the current path if we are inside one. None
        otherwise.
        """

    def getSingleEntryPoints():
        """ Retrieve all sections implementing ISubsite that match the local
        Subjects.
        """

    def getSingleEntryPointsBySubject(subjects):
        """ Retrieve all sections implementing ISubsite that match the local
        Subjects.
        """

    def getGermanNetwork():
        """ returns the sites from the European Network """

    def getEuropeanNetwork():
        """ returns the sites from the European Network """

    def getInternationalNetwork():
        """ returns the sites from the European Network """

    def handleOSHMailUrls(text, id=''):
        """ turn relative URLs into absolute URLs based on the context's
        URL; append google analytics code.
        """

    def makeAbsoluteUrls(text):
        """ make absolute urls out of relative urls """

    def subsiteRootUrl():
        """ return URL of subsite """

    def subsiteRootPath():
        """ return path of subsite """

    def getBase_url():
        """ Returns a (sub-) sites URL including the language folder
        if present """

    def isSubsite(site):
        """is the site a subsite?"""

    def get_subsite_property(name):
        """ return the prop with name from the subsite """

    def set_subsite_property(name, value):
        """ Set a prop with the name to value on the subsite """

    def getCalendarEvents(start, stop, reverse):
        """ If called on a calendar, the list of events is returned"""

    def getLocalObject(name):
        """returns object with given name from local context or None.
        No Acquisition
        """

    def get_sorted(collection, key=None, reverse=False):
        """Allows sorted() to be used from any page template"""

    def get_native_language_by_code(lang_code):
        """Returns the localized name of a language for a given language code
        """

    def inlinestyler(data):
        """ calls an external service to integrate styles into tags """

    def collage2table(data):
        """ takes an html page generated from collage in the oshmail format
        and converts some divs to a table layout the collage builds a system
        of nested divs for rows and columns. What we need is a table with two
        rows. The first row contains two columns, the second one only one.

        into 1.1 and 1.2 we put the content of the div.content-column
        into 2.1 we put the div.collage-row>div.collage-row
        """

class IOSHAHeaderTopactions(IViewletManager):
    """A viewlet manager that sits in the portal-header and wraps top actions
    """

class IEsenerPortalTop(IViewletManager):
    """ For Esener, we only want to show a limited amount of portles in the portal top
    """

class IOSHAHeaderEsener(IViewletManager):
    """A viewlet manager that sits in the portal-header and wraps top actions for Esener
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

class IOSHContentSwitcher(Interface):
    """Switch content type of OSH content (form)"""

class ISwitchOSHContent(Interface):
    """Switch content type of OSH content (executing method)"""

class IInlineContentViewlet(Interface):
    """ Marker interface that makes the InlineContentViewlet visible """

class ICompetitionsView(Interface):
    """ Overview of all competitions """

class ICompetitionDetail(Interface):
    """ Detail view of one competition """

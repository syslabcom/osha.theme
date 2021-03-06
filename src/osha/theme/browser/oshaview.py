from urlparse import urljoin
from types import *
import logging
#import urllib2
from BeautifulSoup import BeautifulSoup, Tag

import Acquisition

from zope.i18n import translate
from zope.interface import implements

from plone.memoize import ram

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import getSiteEncoding
from Products.Five import BrowserView
from Products.validation import validation

from gocept.linkchecker.utils import retrieveHTML, retrieveSTX
# from p4a.calendar import interfaces as p4aCalendarInterfaces
from slc.subsite.interfaces import ISubsiteEnhanced
from slc.subsite.root import getSubsiteRoot

from osha.policy.interfaces import ISingleEntryPoint
from osha.theme.browser.interfaces import IOSHA
from osha.theme.browser.osha_properties_controlpanel import \
    PropertiesControlPanelAdapter
from osha.theme.config import *
from osha.theme.cssselect import Converter

logger = logging.getLogger("oshaview")


class OSHA(BrowserView):
    implements(IOSHA)

    def cropHtmlText(self, text, length, ellipsis=u'...'):
        """ first strip html, then crop """
        context = Acquisition.aq_inner(self.context)
        portal_transforms = getToolByName(context, 'portal_transforms')
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        try:
            text = portal_transforms.convert('html_to_text', text).getData()
            text = text.decode('utf-8')
        except Exception, err:
            logger.error(
                'An error occurred in cropHTMLText, original text: %s, '
                'message: %s URL: %s' % (
                    str([text]), str(err), context.absolute_url()
                )
            )
            return text
        return context.restrictedTraverse('@@plone').cropText(
            text, length, ellipsis)

    def _render_cachekey_getSEPs(method, self):
        preflang = getToolByName(
            self.context, 'portal_languages').getPreferredLanguage()
        url = self.context.REQUEST.get('SERVER_URL')
        return (preflang, url)

    @ram.cache(_render_cachekey_getSEPs)
    def getSingleEntryPoints(self):
        """ Retrieve all sections implementing ISingleEntryPoint that match
            the local Subjects
        """
        portal_catalog = getToolByName(self, 'portal_catalog')
        sections = portal_catalog(
            object_provides='osha.policy.interfaces.ISingleEntryPoint',
            review_state="published"
        )
        rs = []
        for section in sections:
            rs.append(dict(
                title=section.Title, url=section.getURL(),
                subject=section.Subject,
            ))
        rs.sort(lambda x, y: cmp(x['title'].lower(), y['title'].lower()))
        return rs

    def get_subsite_property(self, name):
        """ return the prop with name from the subsite """
        subsite_path = self.subsiteRootPath()
        subsite = self.context.restrictedTraverse(subsite_path)
        P = PropertiesControlPanelAdapter(subsite)
        return getattr(P, name, None)

    def set_subsite_property(self, name, value):
        """ Set a prop with the name to value on the subsite """
        subsite_path = self.subsiteRootPath()
        subsite = self.context.restrictedTraverse(subsite_path)
        P = PropertiesControlPanelAdapter(subsite)
        if hasattr(P, name):
            setattr(P, name, value)

    def getSingleEntryPointsBySubject(self, subjects):
        """ Retrieve all sections implementing ISubsite that match the
            local Subjects
        """
        seps = self.getSingleEntryPoints()
        seplist = []
        for sep in seps:
            S = sep['subject']
            if not S:
                continue
            for subject in S:
                if subject in subjects:
                    seplist.append(sep)
                    continue

        seplist.sort(lambda x, y: cmp(x['title'].lower(), y['title'].lower()))
        return seplist

    def getCurrentSingleEntryPoint(self):
        """ returns the SEP in the current path if we are inside one.
            None otherwise """
        PARENTS = self.request.PARENTS
        for parent in PARENTS:
            if ISingleEntryPoint.providedBy(parent):
                return parent
        return None

    def getCurrentSubsite(self):
        """ returns the subsite in the current path if we are inside one.
            None otherwise """
        PARENTS = self.request.PARENTS
        for parent in PARENTS:
            if ISubsiteEnhanced.providedBy(parent):
                return parent
        return None

    def getPageShareImageSource(self):
        """ Return the path for the image that will be shared with the addthis
            button.
        """
        context = Acquisition.aq_inner(self.context)
        if hasattr(context.aq_explicit, 'getImage'):
            return "%s/image" % (context.absolute_url())
        return ''

    def sendto(self, send_to_address, send_from_address, comment,
               subject='Plone', **kwargs):
        """Sends a link of a page to someone."""
        context = self.context
        host = getToolByName(context, 'MailHost')
        if 'template' in kwargs:
            template = getattr(context, kwargs['template'])
        else:
            template = getattr(context, 'sendto_template')

        portal = getToolByName(context, 'portal_url').getPortalObject()
        encoding = portal.getProperty('email_charset')
        msg_type = kwargs.get('msg_type', 'text/plain')
        if 'envelope_from' in kwargs:
            envelope_from = kwargs['envelope_from']
        else:
            envelope_from = send_from_address
        # Cook from template
        message = template(
            context, send_to_address=send_to_address,
            send_from_address=send_from_address, comment=comment,
            subject=subject, **kwargs
        )
        host.send(
            message, mto=send_to_address, mfrom=envelope_from,
            subject=subject, msg_type=msg_type, charset=encoding
        )

    def getTranslatedCategories(self, domain='osha'):
        """ returns a list of tuples, that contain key and title of
            Categories (Subject) ordered by Title """
        IGNORE = ['provider']
        pc = getToolByName(self.context, 'portal_catalog')
        plt = getToolByName(self.context, 'portal_languages')
        lang = plt.getPreferredLanguage()
        usedSubjects = pc.uniqueValuesFor('Subject')
        subjects = list()
        for s in usedSubjects:
            if s in IGNORE:
                continue
            subjects.append((
                s, translate(target_language=lang, msgid=s, default=s,
                            context=self.context, domain=domain)
            ))
        subjects.sort(lambda x, y: cmp(x[1], y[1]))

        return subjects

    def getGermanNetwork(self):
        """ returns the sites from the European Network """
        return GERMAN_NETWORK

    def getDutchNetwork(self):
        """ returns the sites from the European Network """
        return DUTCH_NETWORK

    def getEuropeanNetwork(self):
        """ returns the sites from the European Network """
        return EUROPEAN_NETWORK

    def getInternationalNetwork(self):
        """ returns the sites from the European Network """
        return INTERNATIONAL_NETWORK

    def retrieveLinksFromHTML(self, text):
        """ The method retrieveHTML provided by gocept.linkchecker is NOT
        reliable. It fails to find more than one relative link inside a given
        text. Therefore we build our own link exctractor based on BeautifulSoup
        """
        soup = BeautifulSoup(text)
        links = soup.findAll('a')
        return [x.get('href', '').encode('utf-8') for x in links]

    def handleOSHMailUrls(self, text, id=''):
        """ turn relative URLs into absolute URLs based on the context's URL;
            append google analytics code
        """
        encoding = getSiteEncoding(self)
        if type(text) == unicode:
            text = text.encode(encoding)
        links = []
        isURL = validation.validatorFor('isURL')
        if isURL(text) == 1:
            links.append(text)
        else:
            for link in retrieveSTX(text):
                links.append(link)

            for link in self.retrieveLinksFromHTML(text):
                links.append(link)

        au = self.context.absolute_url()
        for link in links:
            if not link.startswith('mailto'):
                joinchar = link.find('?') > 0 and '&' or '?'
                newlink = "%(link)s%(joinchar)sutm_source=oshmail&"\
                    "utm_medium=email&utm_campaign=%(campaign)s" % dict(
                    link=urljoin(au, link), joinchar=joinchar,
                    campaign=id != '' and id or 'oshmail')
                # below is a fix for the problem that you have two links in
                # text, one being a prefix of the
                # other and appearing below it. In this case, the smaller
                # one will be replaced with GA postfix in the longer one
                # as fix, only replace links which terminate with a ".
                # Of course this requires that all links are closed properly
                # if the text already is a URL however, we don't want this hack
                if isURL(text) == 1:
                    text = text.replace(link, newlink)
                else:
                    text = text.replace(link + '"', newlink + '"')
        text = text.decode(encoding)
        return text

    def makeAbsoluteUrls(self, text):
        """ turn relative URLs into absolute URLs
            based on the context's URL """
        links = []

        for link in retrieveSTX(text):
            links.append(link)

        for link in retrieveHTML(text):
            links.append(link)

        au = self.context.absolute_url()
        for link in links:
            if not link.startswith('mailto'):
                #text = text.replace(link, urljoin(au, link))
                joinchar = link.find('?') > 0 and '&' or '?'
                newlink = "%(link)s%(joinchar)sutm_source=shortmessage&"\
                    "utm_medium=email&utm_campaign=%(campaign)s" % dict(
                    link=urljoin(au, link), joinchar=joinchar,
                    campaign='shortmessage')
                # below is a fix for the problem that you have two links in
                # text, one being a prefix of the
                # other and appearing below it. In this case, the smaller
                # one will be replaced with GA postfix in the longer one
                # as fix, only replace links which terminate with a ".
                # Of course this requires that all links are closed properly
                # if the text already is a URL however, we don't want this hack
                text = text.replace(link + '"', newlink + '"')
        return text

    def subsiteRootPath(self):
        """ return URL of subsite """
        return getSubsiteRoot(Acquisition.aq_inner(self.context))

    def subsiteRootUrl(self):
        """ return path of subsite """
        rootPath = self.subsiteRootPath()
        return self.request.physicalPathToURL(rootPath)

    def isSubsite(self, site):
        return ISubsiteEnhanced.providedBy(site)

    def getBase_url(self):
        """ Returns a (sub-) sites URL including the language folder
        if present """
        language = getToolByName(
            self.context, 'portal_languages').getPreferredLanguage()
        subsite_url = self.subsiteRootUrl()
        subsite_path = self.subsiteRootPath()
        root = self.context.restrictedTraverse(subsite_path)
        if hasattr(Acquisition.aq_base(Acquisition.aq_inner(root)), language):
            base_url = '%s/%s' % (subsite_url, language)
        else:
            base_url = subsite_url
        return base_url

    def getCalendarEvents(self, past=False):
        """ If called on a calendar, the list of events is returned"""
        # context = self.context
        # XXX Fixme: replacement for p4a.calendar
        # if p4aCalendarInterfaces.ICalendarEnhanced.providedBy(context):
        #     now = datetime.datetime.now()
        #     if past:
        #         stop = now
        #         start = None
        #     else:
        #         start = now
        #         stop = None
        #     provider = p4aCalendarInterfaces.IEventProvider(self.context)
        #     events = list(provider.gather_events(start=start, stop=stop))
        #     events.sort()
        #     if past:
        #         events.reverse()
        #     events = [brain._getEvent() for brain in events]
        #     return events
        return list()

    def getLocalObject(self, name):
        """ see interface """
        return hasattr(
            Acquisition.aq_base(Acquisition.aq_inner(self.context)), name
        ) and getattr(self.context, name) or None

    def getNumAlertSubscribers(self):
        """ This is the same as num_subscribers in portlets/alertservice.py
        Copied here so we can access it from a page template. #1330
        """
        context = Acquisition.aq_inner(self.context)
        portal_alerts = getToolByName(context, 'portal_alertservice')
        try:
            n = len(portal_alerts.nprofiles.objectIds())
        except:
            n = ''
        return n

    def get_sorted(self, collection, key=None, reverse=False):
        """Allows sorted() to be used from any page template"""
        return sorted(collection, key=key, reverse=reverse)

    def get_native_language_by_code(self, lang_code):
        context = self.context
        ltool = context.portal_languages
        lang_info = ltool.getAvailableLanguageInformation().get(
            lang_code, None)
        if lang_info is not None:
            return lang_info.get(u"native", None)
        return None

    def get_orientation(self, image):
        width_str = image.getWidth()
        height_str = image.getHeight()
        try:
            width = int(width_str)
            height = int(height_str)
        except (ValueError, TypeError):
            return ""
        if height == 0:
            return ""
        elif width / height < 1:
            return "portrait"
        else:
            return "landscape"

    def pdb_from_page_template(self, *args, **kwargs):
        import pdb
        pdb.set_trace()

    def inlinestyler(self, data):
        """ calls an external service to integrate styles into tags """
        # service_url = "http://inlinestyler.torchboxapps.com/styler/convert/"
        # params = dict(returnraw='1', source=data.encode('utf8'))
        # req = urllib2.Request(url=service_url, data=urllib.urlencode(params))
        # f = urllib2.urlopen(req)

        # ret = BeautifulSoup(
        #     f.read(), convertEntities=BeautifulSoup.HTML_ENTITIES)
        # return ret.text
        converter = Converter()
        text = converter.perform(data)
        if not isinstance(text, unicode):
            text = text.decode('utf-8')
        return text

    def collage2table(self, data, u=False):
        """
        Takes an html page generated from collage in the oshmail format and
        converts some divs to a table layout. The collage builds a system
        of nested divs for rows and columns. What we need is a table with
        one row, with two columns: 1.1 and 1.2.
        """
        soup = BeautifulSoup(data)

        # find the real content cells
        cell_11, cell_12 = soup.findAll(
            attrs={'class': 'collage-column'}, limit=2)

        # create a table
        table = Tag(soup, "table", [("id", 'collage-table')])

        row1 = Tag(soup, "tr")
        row2 = Tag(soup, "tr")

        col1 = Tag(soup, "td", [
            ("valign", "top"), ("id", "collage-table-cell1"),
            ("width", "590")
        ])
        col2 = Tag(soup, "td", [
            ("valign", "top"), ("id", "collage-table-cell2"), ("width", "200")
        ])

        col1.insert(0, cell_11)
        col2.insert(0, cell_12)

        row1.insert(0, col1)
        row1.insert(1, col2)

        table.insert(0, row1)

        if u:
            return unicode(table)
        return str(table)

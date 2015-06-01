from BeautifulSoup import BeautifulSoup
from cgi import escape
import types

from zope.app.component.hooks import getSite
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.i18n import translate
from Acquisition import aq_base, aq_inner, aq_parent
from ZTUtils import make_query

from AccessControl.SecurityManagement import getSecurityManager
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from Products.LinguaPlone.interfaces import ITranslatable
from zope.annotation.interfaces import IAnnotations, IAnnotatable

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress

from plone.app.layout.viewlets import common
from plone.app.portlets.cache import get_language

from slc.subsite.interfaces import ISubsiteEnhanced
from Products.CMFPlone.utils import isExpired
from Products.RemoteProvider.content.interfaces import IProvider
from Products.OSHContentLink.interfaces import IOSH_Link
from slc.googlesearch.interfaces import IGoogleSearchSettings
from plone.app.layout.viewlets.common import DublinCoreViewlet

from osha.theme import config
from osha.theme.browser.interfaces import IInlineContentViewlet
from osha.theme.browser.osha_properties_controlpanel import PropertiesControlPanelAdapter
from osha.theme.browser.topics_view import TopicsBrowserView
from slc.outdated.viewlet import OutdatedViewlet as OutdatedViewletBase
from slc.outdated import Outdated


class OSHALanguageSelector(TranslatableLanguageSelector):
    """ Override LinguaPlone's language selector to provide our own template
        This is used for content that is LinguaPlone translatable """

    _template = ViewPageTemplateFile('templates/languageselector.pt')

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        return (navigation_root_path, preflang)

    #@ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def languages(self):
        context = aq_inner(self.context)
        results = super(OSHALanguageSelector, self).languages()
        supported_langs = [v['code'] for v in results]
        missing = set([str(c) for c in supported_langs])
        translations = self._translations(missing)
        # On the main portal, we want to be able to filter out unwanted
        # languages needes for subsites
        oshaview = getMultiAdapter((self.context, self.request), name='oshaview')
        subsite_path = oshaview.subsiteRootPath()
        potential_subsite = self.context.restrictedTraverse(subsite_path)
        append_path = self._findpath(context.getPhysicalPath(),
                                     self.request.get('PATH_INFO', ''))
        formvariables = self._formvariables(self.request.form)
        _checkPermission = getSecurityManager().checkPermission

        # only interesting on the main portal
        # or on subsites without their own language tool
        if not ISubsiteEnhanced.providedBy(potential_subsite) \
            or (ISubsiteEnhanced.providedBy(potential_subsite) \
                and not getattr(aq_base(potential_subsite), 'portal_languages', None)):
            portal_properties = getToolByName(self.context, 'portal_properties')
            site_properties = getattr(portal_properties, 'site_properties')
            languages_on_main_site = getattr(site_properties, 'languages_on_main_site', None)
            if languages_on_main_site:
                results = [x for x in results if x['code'] in languages_on_main_site]

        # Starting here, we just copy from LinguaPlone
        non_viewable = set()
        for data in results:
            code = str(data['code'])
            data['translated'] = code in translations.keys()
            set_language = '?set_language=%s' % code

            try:
                appendtourl = '/'.join(append_path)
                if self.set_language:
                    appendtourl += '?' + make_query(formvariables,
                                                    dict(set_language=code))
                elif formvariables:
                    appendtourl += '?' + make_query(formvariables)
            except UnicodeError:
                appendtourl = '/'.join(append_path)
                if self.set_language:
                    appendtourl += set_language

            if data['translated']:
                trans, direct, has_view_permission = translations[code]
                if not has_view_permission:
                    # shortcut if the user cannot see the item
                    non_viewable.add((data['code']))
                    continue

                state = getMultiAdapter((trans, self.request),
                        name='plone_context_state')
                if direct:
                    data['url'] = state.canonical_object_url() + appendtourl
                else:
                    data['url'] = state.canonical_object_url() + set_language
            else:
                has_view_permission = bool(_checkPermission('View', context))
                # Ideally, we should also check the View permission of default
                # items of folderish objects.
                # However, this would be expensive at it would mean that the
                # default item should be loaded as well.
                #
                # IOW, it is a conscious decision to not take in account the
                # use case where a user has View permission a folder but not on
                # its default item.
                if not has_view_permission:
                    non_viewable.add((data['code']))
                    continue

                state = getMultiAdapter((context, self.request),
                        name='plone_context_state')
                try:
                    data['url'] = state.canonical_object_url() + appendtourl
                except AttributeError:
                    data['url'] = context.absolute_url() + appendtourl

        # filter out non-viewable items
        results = [r for r in results if r['code'] not in non_viewable]
        return results

class OSHAGermanyLanguageSelector(OSHALanguageSelector):
    """ Override OSHA language selector to provide a german template
        This is used for content that is LinguaPlone translatable """
    _template = ViewPageTemplateFile('templates/languageselector_de.pt')

    def showFlags(self):
        return True


class OSHASiteActionsViewlet(common.SiteActionsViewlet):

    render = ViewPageTemplateFile('templates/site_actions.pt')

    def get_site_slogan(self):
        """ return the site or subsite slogan """
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        defaultlang = getToolByName(self.context, 'portal_languages').getDefaultLanguage()

        oshaview = getMultiAdapter((self.context, self.request), name='oshaview')
        subsite_path = oshaview.subsiteRootPath()
        subsite = self.context.restrictedTraverse(subsite_path)
        P = PropertiesControlPanelAdapter(subsite)
        slogans = [(x.language, x.text) for x in P.site_slogan]
        slogans = dict(slogans)
        return slogans.get(preflang, slogans.get(defaultlang, 'European Agency for Safety and Health at Work'))


class OSHANetworkchooser(common.ViewletBase):

    _template = ViewPageTemplateFile('templates/network_chooser.pt')

    def _render_cachekey(method, self):
        preflang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        oshaview = getMultiAdapter((self.context, self.request), name='oshaview')
        subsite_path = oshaview.subsiteRootPath()
        return (subsite_path, preflang)

    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def networks(self):
        """ returns a list of networks for display depending on the current subsite """
        oshaview = getMultiAdapter((self.context, self.request), name='oshaview')
        subsite_path = oshaview.subsiteRootPath()

        if subsite_path.split('/')[-1]=='germany':
            return (self.de(),)

        else:
            return tuple()

    def de(self):
        """ returns the sites from the European Network """
        return dict(title='German Network',
                    id='deNetwork',
                    sites=config.GERMAN_NETWORK)

    def nl(self):
        """ returns the sites from the European Network """
        return dict(title='Dutch Network',
                    id='nlNetwork',
                    sites=config.DUTCH_NETWORK)

    def eu(self):
        """ returns the sites from the European Network """
        return dict(title='European Network',
                    id='euNetwork',
                    sites=config.EUROPEAN_NETWORK)

    def int(self):
        """ returns the sites from the European Network """
        return dict(title='International Network',
                    id='intNetwork',
                    sites=config.INTERNATIONAL_NETWORK)

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        self.action = self.context.absolute_url() + '/global_network'


class OSHAPathBarViewlet(common.PathBarViewlet):

    render =  ViewPageTemplateFile('templates/path_bar.pt')

    @property
    def is_lang_root(self):
        portal = getSite()
        lang = getToolByName(
            self.context, 'portal_languages').getPreferredLanguage()
        portal_lang = portal.get(lang)
        if portal_lang is None:
            # This can only happen for a bare test instance
            return False
        default_site_root_page = portal_lang.getDefaultPage()
        if default_site_root_page is None:
            if self.context == portal_lang:
                return True
        elif self.context == portal_lang.get(default_site_root_page, None):
            return True
        else:
            return False

    def update(self):
        super(common.PathBarViewlet, self).update()

        self.navigation_root_url = self.portal_state.navigation_root_url()

        self.is_rtl = self.portal_state.is_rtl()

        breadcrumbs_view = getMultiAdapter((self.context, self.request),
                                           name='breadcrumbs_view')
        self.breadcrumbs = breadcrumbs_view.breadcrumbs()


class OSHAEsenerPathBarViewlet(OSHAPathBarViewlet):

    def update(self):
        super(OSHAPathBarViewlet, self).update()
        context = self.context
        # ptool = getToolByName(self.context, 'portal_url')
        # portal = ptool.getPortalObject()
        # osha_view = getMultiAdapter((self.context, self.context.REQUEST), name=u'oshaview')
        lang = getToolByName(
            self.context, 'portal_languages').getPreferredLanguage()
        # portal_lang = portal.get(lang, portal.get('en'))

        # self.navigation_root_url = "/".join(portal_lang.getPhysicalPath())
        # self.navigation_root_url = "/sub/esener/{0}".format(lang)
        self.navigation_root_url = self.context.absolute_url()
        self.breadcrumbs = (dict(
            absolute_url=context.absolute_url(), Title=context.Title(),
        ),)


class OSHAFopPathBarViewlet(OSHAPathBarViewlet):

    def update(self):
        super(OSHAPathBarViewlet, self).update()
        context = self.context
        ptool = getToolByName(self.context, 'portal_url')
        portal = ptool.getPortalObject()
        lang = getToolByName(
            self.context, 'portal_languages').getPreferredLanguage()
        portal_lang = portal.get(lang, portal.get('en'))
        self.navigation_root_url = "/".join(portal_lang.getPhysicalPath())

        breadcrumbs = list()
        network = portal_lang.get('oshnetwork', None)
        if network:
            breadcrumbs.append(dict(
                absolute_url=network.absolute_url(), Title=network.Title(),
            ))
        breadcrumbs.append(dict(
            absolute_url=context.absolute_url(), Title=context.Title(),
        ))
        self.breadcrumbs = tuple(breadcrumbs)


class OSHACampaignAreaViewlet(common.ViewletBase):

    render =  ViewPageTemplateFile('templates/osha_campaignarea.pt')

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        langtool = getToolByName(self.context, 'portal_languages', None)
        current_lang = langtool.getPreferredLanguage()

        self.navigation_root_url = portal_state.navigation_root_url()

        portal = portal_state.portal()

        logoName = ''

        if(hasattr(portal.restrictedTraverse('base_properties'), 'campaignLogoName')):
            logoName = portal.restrictedTraverse('base_properties').campaignLogoName

        #self.campaign_logo_tag = ''
        if logoName != '':
            if current_lang != 'en':
                file_name = logoName.split(".")
                file_name[0] = file_name[0] + "_" + current_lang
                logoName = ".".join(file_name)


        self.campaign_logo_name = logoName
        self.campaign_logo_url = '%s/%s' % (self.navigation_root_url, logoName)

class OSHACampaignArea2Viewlet(common.ViewletBase):

    render =  ViewPageTemplateFile('templates/osha_campaignarea2.pt')

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        langtool = getToolByName(self.context, 'portal_languages', None)
        bound = langtool.getLanguageBindings()
        current_lang = bound[0]

        self.navigation_root_url = portal_state.navigation_root_url()


        portal = portal_state.portal()

        logoName = ''

        if(hasattr(portal.restrictedTraverse('base_properties'), 'campaignLogo2Name')):
            logoName = portal.restrictedTraverse('base_properties').campaignLogo2Name

        if logoName != '':
            if current_lang != 'en':
                file_name = logoName.split(".")
                file_name[0] = file_name[0] + "_" + current_lang
                logoName = ".".join(file_name)


        self.campaign_logo2_name = logoName
        self.campaign_logo2_url = '%s/%s' % (self.navigation_root_url, logoName)

class OSHAFooterLanguageSelector(TranslatableLanguageSelector):

    render = ViewPageTemplateFile('templates/footer_languageselector.pt')


class OSHAFooterActions(common.ViewletBase):

    _template = ViewPageTemplateFile('templates/footer_actions.pt')

    def _footer_render_details_cachekey(fun, self):
        """
        Generates a key based on:

        * Current URL
        * Negotiated language
        * Anonymous user flag

        """
        context = aq_inner(self.context)

        anonymous = getToolByName(context, 'portal_membership').isAnonymousUser()

        key= "".join((
            '/'.join(aq_inner(self.context).getPhysicalPath()),
            get_language(aq_inner(self.context), self.request),
            str(anonymous),
            ))
        return key

    @ram.cache(_footer_render_details_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def update(self):
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')

        self.portal = portal_state.portal()
        self.site_url = portal_state.portal_url()

        self.portal_actionicons = aq_base(getToolByName(self.context, 'portal_actionicons'))

        self.document_actions = context_state.actions().get('document_actions', None)
        self.footer_actions = context_state.actions().get('footer_actions', None)
        self.site_actions = context_state.actions().get('site_actions', None)

        plone_utils = getToolByName(self.context, 'plone_utils')
        self.getIconFor = plone_utils.getIconFor

    def icon(self, action):
        return self.getIconFor('plone', action['id'], None)

class OSHALogoViewlet(common.LogoViewlet):

    render = ViewPageTemplateFile('templates/logo.pt')

    def preflang(self):
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        return portal_state.locale().getLocaleID()

    def getLink(self):
        osha_view = getMultiAdapter((self.context, self.request), name=u'oshaview')
        link = osha_view.get_subsite_property('link_on_logo')
        protocol = self.request.get('SERVER_URL').split(':')[0]
        protocol = protocol == "https" and protocol or "http"
        if link:
            if ":" in link:
                link = link.split(':')[1:][0]
        if link:
            if not link.startswith('//'):
                link = "//%s" % link
        else:
            link = '//osha.europa.eu'
        link = '%s:%s' % (protocol, link)
        return link

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        langtool = getToolByName(self.context, 'portal_languages', None)
        bound = langtool.getLanguageBindings()
        current_lang = bound[0]

        self.navigation_root_url = portal_state.navigation_root_url()

        portal = portal_state.portal()
        osha_view = getMultiAdapter((self.context, self.context.REQUEST), name=u'oshaview')
        subsite = portal.restrictedTraverse(osha_view.subsiteRootPath())
        logoName = subsite.restrictedTraverse('base_properties').logoName

        self.logo_tag = subsite.restrictedTraverse(logoName).tag()
        if current_lang != 'en':
            try:
                init = logoName
                file_name = init.split(".")
                file_name[0] = file_name[0] + "_" + current_lang
                logoName = ".".join(file_name)
                self.logo_tag = subsite.restrictedTraverse(logoName).tag()
            except:
                pass

        self.portal_title = portal_state.portal_title()

class TitleViewlet(common.TitleViewlet):
    """ overwritten from plone.app.layout """

    def render(self):
        portal_state = getMultiAdapter((self.context, self.request),
            name=u'plone_portal_state')
        context_state = getMultiAdapter((self.context, self.request),
            name=u'plone_context_state')
        page_title = escape(safe_unicode(context_state.object_title()))
        portal_title = escape(safe_unicode(portal_state.navigation_root_title()))
        portal_title = safe_unicode(translate(portal_title, domain='osha'))
        page_title = safe_unicode(page_title)
        osha = safe_unicode(translate('OSHA', domain='osha'))
        if page_title == portal_title:
            return u"<title>%s</title>" % (escape(portal_title))
        else:
            return u"<title>%s &mdash; %s</title>" % (
                escape(safe_unicode(page_title)),
                escape(safe_unicode(portal_title)))


class OSHANapoHeadViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/napo_head.pt')

class OSHANapoSubHeadViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/napo_subhead.pt')

class OSHANapoBelowFooterViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/napo_belowfooter.pt')

class AddThisButtonViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/addthis.pt')


class OSHAContentSwitcherViewlet(common.ViewletBase):

    def showeditbox(self):
        user = getToolByName(self.context, 'portal_membership').getAuthenticatedMember()
        if user.has_role(('Manager', 'Reviewer')):
            return True
        return False

    def getUID(self):
        return self.context.UID()

    def getExisting(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        if not IAnnotatable.providedBy(self.context):
            return ''
        ann = IAnnotations(self.context)
        existing_uid = ann.get(config.EXISTING_SWITCHED_CONTENT_UID, '')
        existing_url = ''
        if existing_uid:
            res = portal_catalog(UID=existing_uid)
            existing = len(res) and res[0].getObject()
            existing_url = existing and existing.absolute_url()
        return existing_url


class ProviderToOSHLinkViewlet(OSHAContentSwitcherViewlet):

    render = ViewPageTemplateFile('templates/provider_to_oshlink.pt')

    def show(self):
        if not IProvider.providedBy(self.context):
            return False
        qi = getToolByName(self.context, 'portal_quickinstaller')
        if not qi.isProductInstalled('Products.RemoteProvider'):
            return False
        user = getToolByName(self.context, 'portal_membership').getAuthenticatedMember()
        if user.has_role(('Manager', 'Reviewer')):
            return True
        return False


class OSHLinkToProviderViewlet(OSHAContentSwitcherViewlet):

    render = ViewPageTemplateFile('templates/oshlink_to_provider.pt')

    def show(self):
        if not IOSH_Link.providedBy(self.context):
            return False
        qi = getToolByName(self.context, 'portal_quickinstaller')
        if not qi.isProductInstalled('Products.OSHContentLink'):
            return False
        user = getToolByName(self.context, 'portal_membership').getAuthenticatedMember()
        if user.has_role(('Manager', 'Reviewer')):
            return True
        return False


class InlineContentViewlet(common.ViewletBase):

    render = ViewPageTemplateFile('templates/inline_content_viewlet.pt')

    def showeditlink(self):
        user = getToolByName(self.context, 'portal_membership').getAuthenticatedMember()
        if user.has_role(('Manager', 'Reviewer')):
            return True
        return False

    def getContentObject(self):
        return getattr(self.context, config.INLINE_CONTENT_VIEWLET_NAME, None)

    def show(self):
        if not IInlineContentViewlet.providedBy(self.context):
            return False
        if not self.getContentObject():
            return False
        return True


class TopicViewHeading(common.ViewletBase, TopicsBrowserView):
    render = ViewPageTemplateFile('templates/topic_view_heading_viewlet.pt')


class GoogleSearchViewlet(common.ViewletBase):
    render = ViewPageTemplateFile('templates/googlesearch_viewlet.pt')

    def update(self):
        self.language = getToolByName(self.context, 'portal_languages').getPreferredLanguage()

        purl = getToolByName(self.context, 'portal_url')
        portal = purl.getPortalObject()
        self.portal_path = '/'.join(portal.getPhysicalPath())
        osha_view = getMultiAdapter((self.context, self.request), name=u'oshaview')
        self.subsite_url = osha_view.subsiteRootUrl()
        self.subsite_path = osha_view.subsiteRootPath()

    def index_alphabetical(self):
        return '%s/%s/@@index_alphabetical' %(self.subsite_url, self.language)

    def showAtozLink(self):
        # shortcut, don't show alphabetical search #4155 comment 18
        return False

        osha_view = getMultiAdapter((self.context, self.request), name=u'oshaview')
        show = osha_view.get_subsite_property('show_atoz_link')
        if show is None:
            show = True
        return show

    def oshGlobalSearchLink(self):
        return '%s/%s/slc_cse_search_results' %(self.subsite_url, self.language)

    def enable_livesearch(self):
        return False

    def getCSE(self):
        GSS = getUtility(IGoogleSearchSettings)
        # just pick the first setting...
        for setting in GSS.stored_settings:
            value = "cx::%s" %(setting.cx)
            return value
        return "::"

    def getCx(self):
        try:
            typus, value = self.getCSE().split('::')
            if typus=='cx':
                return value
        except ValueError:
            pass
        return ''

    def getLanguage(self):
        return self.language

    def getAdditional(self):
        return ""

    #@memoize
    def _get_base_url(self):
        root = self.context.restrictedTraverse(self.portal_path)
        if hasattr(aq_base(aq_inner(root)), self.language):
            return '%s/%s' %(root.absolute_url(), self.language)
        else:
            return root.absolute_url()

    @property
    def search_action(self):
        base_url = self._get_base_url()
        return '%s/site_search' % base_url


class OSHADublinCoreViewlet(DublinCoreViewlet):

    def listMetaTags(self, context):
        """ retrieve the metadata for the header and make osha specific
            additions """
        EASHW = 'European Agency for Safety and Health at Work'

        putils = getToolByName(context, 'plone_utils')
        portal_state = getMultiAdapter((context, self.request),
            name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        navigation_root = context.restrictedTraverse(navigation_root_path)

        # fetch plone standard
        meta = putils.listMetaTags(context)

        meta['title'] = context.Title()
        meta['DC.title'] = context.Title()

        desc = None
        if shasattr(context, "getField") and context.getField("seoDescription"):
            desc = context.getField("seoDescription").get(context)

        if not desc:
            desc = context.Description() or navigation_root.Description()

        desc = "".join(BeautifulSoup(desc).findAll(text = True))
        meta['description'] = desc
        meta['DC.description'] = desc

        medium = {
                "Image": "image",
                "News Item": "news",
                "Blog Entry": "blog",
                }
        if context.portal_type in medium:
            meta['medium'] = medium.get(context.portal_type)

        Publisher = meta.get('Publisher', None)
        if not Publisher or Publisher == 'No publisher':
            meta['Publisher'] = EASHW

        # Gorka requests on 6.3.2008
        # Just in case, I'd like to remind you the decision we took regarding
        # the keywords for the keywords html tag.
        # The keywords should be added as follows
        # 1.- OSH, OSHA, EU-OSHA, Occupational safety, Occupational health,
        #     European Agency,
        # 2.- plus the osha keywords, plus the thesaurus ones. in that order.

        PREFIX_KEYWORDS = ['OSH', 'OSHA', 'EU-OSHA',
                               'Occupational safety',
                               'Occupational health',
                               'European Agency']

        lang = getToolByName(context,
            'portal_languages').getPreferredLanguage()
        domain = "osha"
        SUBJECT = [translate(target_language=lang, msgid=s, default=s,
            context=context, domain=domain)
            for s in context.Subject()]

        THESAURUS = []
        if hasattr(aq_inner(context), 'getField'):
            field = context.getField('multilingual_thesaurus')
            if field is not None:
                pvt = getToolByName(context, 'portal_vocabularies')
                portal_languages = getToolByName(context, 'portal_languages')
                lang = portal_languages.getPreferredLanguage()
                manager = pvt.MultilingualThesaurus._getManager()

                thesitems = field.getAccessor(context)()
                for thesitem in thesitems:
                    THESAURUS.append(manager.getTermCaptionById(thesitem,
                        lang))

        keywords = PREFIX_KEYWORDS + SUBJECT + THESAURUS
        if isinstance(keywords, (list, tuple)):
            # convert a list to a string
            if keywords is None:
                keywords = ''
            else:
                keywords = [x for x in keywords
                    if type(x) in (types.StringType, types.UnicodeType)]
                keywords = ', '.join(keywords)

        meta['keywords'] = keywords
        meta['DC.subject'] = keywords

        # Creator, Contributor, Rights
        meta['DC.creator'] = EASHW
        meta['DC.contributors'] = EASHW
        meta['DC.rights'] = EASHW

        #Language
        language = context.Language()
        if language:
            meta['DC.language'] = language
            meta['language'] = language

        return meta

    def update(self):
        context = aq_inner(self.context)
        self.metatags = self.listMetaTags(context).items()


class OutdatedViewlet(OutdatedViewletBase):
    """A viewlet that indicates that content is outdated
        If the content item is also expired and the user is not logged in,
        redirect to the parent folder with a 301
    """
    outdated = Outdated()

    def render(self):
        if not self.outdated:
            return ""
        is_anon = getToolByName(self, 'portal_membership').isAnonymousUser()
        if isExpired(self.context) and is_anon:
            parent = aq_parent(self.context)
            self.request.response.redirect(
                "%s?msg=deleted_content&portal_type=%s" % (
                    parent.absolute_url(), self.context.portal_type),
                status=301)
        return super(OutdatedViewlet, self).render()


class ItemDeletedViewlet(common.ViewletBase):
    """ Display a message if the current request has been redirected from
        "deleted" content.
    """

    def render(self):
        if self.request.get('msg', '') == 'deleted_content':
            self.portal_type = self.request.get('portal_type', 'Item')
            return super(ItemDeletedViewlet, self).render()
        return ""

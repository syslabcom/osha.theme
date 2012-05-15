from cgi import escape

from zope.app.component.hooks import getSite
from zope.component import getMultiAdapter
from zope.i18n import translate
from Acquisition import aq_base, aq_inner, aq_parent

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from Products.LinguaPlone.interfaces import ITranslatable
from zope.annotation.interfaces import IAnnotations, IAnnotatable

from plone.memoize import ram
from plone.memoize.compress import xhtml_compress

from plone.app.i18n.locales.browser.selector import LanguageSelector
from plone.app.layout.viewlets import common
from plone.app.portlets.cache import get_language

from slc.subsite.interfaces import ISubsiteEnhanced
from Products.RemoteProvider.content.interfaces import IProvider
from Products.OSHContentLink.interfaces import IOSH_Link

from osha.theme import config
from osha.theme.browser.interfaces import IInlineContentViewlet
from osha.theme.browser.osha_properties_controlpanel import PropertiesControlPanelAdapter

# TODO: Remove the dependency on p4a.plonevideoembed #4414
# from osha.theme.browser.topics_view import TopicsBrowserView

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
        results = LanguageSelector.languages(self)

        # On the main portal, we want to be able to filter out unwanted
        # languages needes for subsites
        oshaview = getMultiAdapter((self.context, self.request), name='oshaview')
        subsite_path = oshaview.subsiteRootPath()
        potential_subsite = self.context.restrictedTraverse(subsite_path)

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

        # for non-translatable content, use standard Plone way of switching language
        if not ITranslatable.providedBy(self.context):
            # special handling for LinguaLinks
            if self.context.getPortalTypeName() == 'LinguaLink':
                can = self.context.getLinkTarget()
                can_lang = can.Language()
                links =  can.getBRefs('lingualink')
                # create a dict that maps language to LinguaLink object
                lang_to_link = dict()
                for link in links:
                    lang_to_link[link.Language()] = link
                for data in results:
                    # for the canonical object, simply link to it
                    if data['code'] == can_lang:
                        data['url'] = can.absolute_url()
                    else:
                        # link to the translation, if present
                        trans = can.getTranslation(data['code'])
                        link = lang_to_link.get(data['code'], None)
                        if trans:
                            data['url'] = trans.absolute_url()
                        # else link to the LinguaLink, if present
                        elif link:
                            data['url'] = link.absolute_url()
                        # or use Plone default language negotiation as a last measure
                        else:
                            data['url'] = self.context.absolute_url()+'/switchLanguage?set_language='+data['code']
                return results
            else:
                for data in results:
                    data['url'] = self.context.absolute_url()+'/switchLanguage?set_language='+data['code']
                return results

        # for translatable content, directly link to the translated objects
        translatable = ITranslatable(self.context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = []
        links =  self.context.getBRefs('lingualink')
        # create a dict that maps language to LinguaLink object
        lang_to_link = dict()
        for link in links:
            lang_to_link[link.Language()] = link

        for data in results:
            data['translated'] = data['code'] in translations
            if data['translated']:
                trans = translations[data['code']][0]
                state = getMultiAdapter((trans, self.request),
                        name='plone_context_state')
                data['url'] = state.view_url() + '?set_language=' + data['code']
            elif data['code'] in lang_to_link:
                data['url'] = lang_to_link[data['code']].absolute_url()
            else:
                state = getMultiAdapter((self.context, self.request),
                        name='plone_context_state')
                try:
                    data['url'] = state.view_url() + '/not_available_lang?set_language=' + data['code']
                except AttributeError:
                    data['url'] = self.context.absolute_url() + '/not_available_lang?set_language=' + data['code']

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

        if subsite_path.split('/')[-1]=='netherlands':
            return (self.nl(),)

        elif subsite_path.split('/')[-1]=='germany':
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
        if link is None:
            link = "https://osha.europa.eu"
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
            return u"<title>%s &mdash; %s &mdash; %s</title>" % (
                escape(safe_unicode(page_title)),
                escape(safe_unicode(osha)),
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
        return getattr(aq_parent(aq_inner(self.context)), config.INLINE_CONTENT_VIEWLET_NAME, None)

    def show(self):
        if not IInlineContentViewlet.providedBy(self.context):
            return False
        if not self.getContentObject():
            return False
        return True

# TODO: Remove the dependency on p4a.plonevideoembed #4414
# class TopicViewHeading(common.ViewletBase, TopicsBrowserView):
#     render = ViewPageTemplateFile('templates/topic_view_heading_viewlet.pt')

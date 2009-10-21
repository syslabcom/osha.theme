from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common
from time import time
from zope.component import getMultiAdapter
from Acquisition import aq_base, aq_inner
from Products.CMFPlone.utils import safe_unicode
from cgi import escape
from plone.memoize.compress import xhtml_compress
from Products.CMFCore.utils import getToolByName
from plone.memoize import ram
from plone.memoize.instance import memoize
from plone.app.portlets.cache import get_language
from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from Products.LinguaPlone.interfaces import ITranslatable
from plone.app.i18n.locales.browser.selector import LanguageSelector
from osha.theme.browser.osha_properties_controlpanel import PropertiesControlPanelAdapter
from slc.subsite.interfaces import ISubsiteEnhanced
from plone.app.layout.navigation.navtree import buildFolderTree

from osha.theme.config import *



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
        return (preflang, subsite_path)
    
    @ram.cache(_render_cachekey)
    def render(self):
        return xhtml_compress(self._template())

    def networks(self):
        """ returns a list of networks for display depending on the current subsite """
        oshaview = getMultiAdapter((self.context, self.request), name='oshaview')
        subsite_path = oshaview.subsiteRootPath()

        if subsite_path.split('/')[-1]=='netherlands':
            return (self.eu(), self.int(), self.nl())

        elif subsite_path.split('/')[-1]=='germany':
            return (self.eu(), self.int(), self.de())

        else:
            return (self.eu(), self.int())

    def de(self):
        """ returns the sites from the European Network """
        return dict(title='German Network', 
                    id='deNetwork', 
                    sites=GERMAN_NETWORK)

    def nl(self):
        """ returns the sites from the European Network """
        return dict(title='Dutch Network', 
                    id='nlNetwork', 
                    sites=DUTCH_NETWORK)
        
    def eu(self):
        """ returns the sites from the European Network """
        return dict(title='European Network', 
                    id='euNetwork', 
                    sites=EUROPEAN_NETWORK)
    
    def int(self):
        """ returns the sites from the European Network """
        return dict(title='International Network', 
                    id='intNetwork', 
                    sites=INTERNATIONAL_NETWORK)
    
    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        context_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_context_state')

        self.action = self.context.absolute_url() + '/global_network'
        
        
class OSHAPathBarViewlet(common.PathBarViewlet):
    
    render =  ViewPageTemplateFile('templates/path_bar.pt')
    
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
            link = "http://osha.europa.eu"
        return link
       
    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        langtool = getToolByName(self.context, 'portal_languages', None) 
        bound = langtool.getLanguageBindings()
        current_lang = bound[0]

        self.navigation_root_url = portal_state.navigation_root_url()

        portal = portal_state.portal()
        osha_view = getMultiAdapter((self.context, self.context.request), name=u'oshaview')
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
        pts = getToolByName(self.context, 'translation_service')
        portal_title = self.portal_title()
        portal_title = safe_unicode(pts.translate(portal_title, domain='osha'))
        page_title = safe_unicode(self.page_title())
        osha = safe_unicode(pts.translate('OSHA', domain='osha'))
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
    
    


        
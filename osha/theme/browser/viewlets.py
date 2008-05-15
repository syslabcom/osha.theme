from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

from zope.component import getMultiAdapter
from Acquisition import aq_base

from Products.CMFCore.utils import getToolByName

from Products.LinguaPlone.browser.selector import TranslatableLanguageSelector
from Products.LinguaPlone.interfaces import ITranslatable
from plone.app.i18n.locales.browser.selector import LanguageSelector

from osha.theme.config import *


class OSHALanguageSelector(TranslatableLanguageSelector):
    """ Override LinguaPlone's language selector to provide our own template
        This is used for content that is LinguaPlone translatable """

    render = ViewPageTemplateFile('templates/languageselector.pt')

    def languages(self):
        results = LanguageSelector.languages(self)
        translatable = ITranslatable(self.context, None)
        if translatable is not None:
            translations = translatable.getTranslations()
        else:
            translations = []

        for data in results:
            data['translated'] = data['code'] in translations
            if data['translated']:
                trans = translations[data['code']][0]
                state = getMultiAdapter((trans, self.request),
                        name='plone_context_state')
                data['url'] = state.view_url() + '?set_language=' + data['code']
            else:
                state = getMultiAdapter((self.context, self.request),
                        name='plone_context_state')
                try:
                    data['url'] = state.view_url() + '/not_available_lang?set_language=' + data['code']
                except AttributeError:
                    data['url'] = self.context.absolute_url() + '/not_available_lang?set_language=' + data['code']

        return results

class OSHASiteActionsViewlet(common.SiteActionsViewlet):

    render = ViewPageTemplateFile('templates/site_actions.pt')


class OSHANetworkchooser(common.ViewletBase):

    render = ViewPageTemplateFile('templates/network_chooser.pt')

    def getGermanNetwork(self):
        """ returns the sites from the European Network """
        return GERMAN_NETWORK
        
    def getEuropeanNetwork(self):
        """ returns the sites from the European Network """
        return EUROPEAN_NETWORK
    
    def getInternationalNetwork(self):
        """ returns the sites from the European Network """
        return INTERNATIONAL_NETWORK
    
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
        # we dont want the first level to show up. This is an easy approach...
#        if len(self.breadcrumbs)>0:
#            self.breadcrumbs = self.breadcrumbs[1:]
                
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
            cLogoName = ''
            if current_lang != 'en':
                try:
                    init = portal.restrictedTraverse('base_properties').campaignLogo2Name
                    file_name = init.split(".")
                    file_name[0] = file_name[0] + "_" + current_lang 
                    cLogoName = ".".join(file_name)
                except:
                    logoName = portal.restrictedTraverse('base_properties').campaignLogo2Name
                    pass
    
            try:
                self.campaign_logo2_tag = portal.restrictedTraverse(cLogoName).tag()
            except:
                self.campaign_logo2_tag = portal.restrictedTraverse(logoName).tag()
                
        else:
            self.campaign_logo2_tag = ''
            
class OSHAFooterLanguageSelector(TranslatableLanguageSelector):

    render = ViewPageTemplateFile('templates/footer_languageselector.pt')
    
class OSHAFooterActions(common.ViewletBase):
    
    render = ViewPageTemplateFile('templates/footer_actions.pt')
    
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

    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        langtool = getToolByName(self.context, 'portal_languages', None) 
        bound = langtool.getLanguageBindings()
        current_lang = bound[0]                                           

        self.navigation_root_url = portal_state.navigation_root_url()

        portal = portal_state.portal()
        
        logoName = portal.restrictedTraverse('base_properties').logoName
        
        if current_lang != 'en':
            try:
                init = portal.restrictedTraverse('base_properties').logoName
                file_name = init.split(".")
                file_name[0] = file_name[0] + "_" + current_lang 
                logoName = ".".join(file_name)
            except:
                pass
        
        self.logo_tag = portal.restrictedTraverse(logoName).tag()

        self.portal_title = portal_state.portal_title()


import Acquisition
from time import time
from osha.theme.browser.interfaces import IOSHA
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.interface import implements, alsoProvides
from plone.memoize.instance import memoize
from plone.memoize import ram
from Products.PlacelessTranslationService import getTranslationService
from osha.theme.config import *
from osha.policy.interfaces import ISingleEntryPoint


class OSHA(BrowserView):
    implements(IOSHA)

    def cropHtmlText(self, text, length, ellipsis='...'):
        """ first strip html, then crop """
        context = Acquisition.aq_inner(self.context)
        portal_transforms = getToolByName(context, 'portal_transforms')
        text = portal_transforms.convert('html_to_text', text).getData()
        return context.restrictedTraverse('@@plone').cropText(text, length, ellipsis)
        
        
    @ram.cache(lambda *args: time() // (60 * 60))
    def getSingleEntryPoints(self):
        """ Retrieve all sections implementing ISubsite that match the local Subjects """
        portal_catalog = getToolByName(self, 'portal_catalog')
        sections = portal_catalog(object_provides='osha.policy.interfaces.ISingleEntryPoint', 
                                  review_state="published")
        rs = []
        for section in sections:
            rs.append(dict(title=section.Title, url=section.getURL(), subject=section.Subject ))
        rs.sort(lambda x,y: cmp(x['title'].lower(), y['title'].lower()))
        return rs        
        
    def getSingleEntryPointsBySubject(self, subjects):
        """ Retrieve all sections implementing ISubsite that match the local Subjects """
        seps = self.getSingleEntryPoints()
        
        seplist = []
        
        for sep in seps:
            S = sep['subject']
            for subject in S:
                if subject in subjects:
                    seplist.append(sep)
                    continue
                    
        seplist.sort(lambda x,y: cmp(x['title'].lower(), y['title'].lower()))
        return seplist
        
    def getCurrentSingleEntryPoint(self):
        """ returns the SEP in the current path if we are inside one. None otherwise """
        PARENTS = self.request.PARENTS
        for parent in PARENTS:
            if ISingleEntryPoint.providedBy(parent):
                return parent
        return None
        
    def listMetaTags(self, context):
        """ retrieve the metadata for the header and make osha specific additions """
        EASHW = 'European Agency for Safety and Health at Work'
        
        putils = getToolByName(context, 'plone_utils')
        # fetch plone standard
        meta = putils.listMetaTags(context)
        
        meta['title'] = context.Title()
        meta['DC.title'] = context.Title()
        
        Publisher = meta.get('Publisher', None)
        if not Publisher or Publisher == 'No publisher':
            meta['Publisher'] = EASHW


        # Gorka requests on 6.3.2008
        # Just in case, I'd like to remind you the decission we took regarding the
        # keywords for the keywords html tag.        
        # The keywords should be added as follows        
        # 1.- OSH, OSHA, EU-OSHA, Occupational safety, Occupational health,
        #     European Agency, 
        # 2.- plus the osha keywords, plus the thesaurus ones. in that order.

        PREFIX_KEYWORDS = ['OSH', 'OSHA', 'EU-OSHA', 
                               'Occupational safety', 
                               'Occupational health',
                               'European Agency']
        SUBJECT = list(context.Subject())

        THESAURUS = []
        if hasattr(Acquisition.aq_inner(context), 'getField'):
            field = context.getField('multilingual_thesaurus')
            if field is not None:
                portal_vocabularies = getToolByName(context, 'portal_vocabularies')
                portal_languages = getToolByName(context, 'portal_languages')        
                lang = portal_languages.getPreferredLanguage()
                manager = portal_vocabularies.MultilingualThesaurus._getManager() 
                
                thesitems = field.getAccessor(context)()
                for thesitem in thesitems:
                    THESAURUS.append(manager.getTermCaptionById(thesitem, lang))


        keywords = PREFIX_KEYWORDS + SUBJECT + THESAURUS
        if isinstance(keywords, (list, tuple)):
            # convert a list to a string
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
        
    
    def sendto(self, send_to_address, send_from_address, comment,
               subject='Plone', **kwargs):
        """Sends a link of a page to someone."""
        context = self.context
        host = getattr(context, 'MailHost')
        if 'template' in kwargs:
            template = getattr(context, kwargs['template'])
        else:
            template = getattr(context, 'sendto_template')

        portal = getToolByName(context, 'portal_url').getPortalObject()
        encoding = portal.getProperty('email_charset')
        subtype = kwargs.get('subtype', 'plain')
        if 'envelope_from' in kwargs:
            envelope_from = kwargs['envelope_from']
        else:
            envelope_from = send_from_address
        # Cook from template
        message = template(context, send_to_address=send_to_address,
                           send_from_address=send_from_address,
                           comment=comment, subject=subject, **kwargs)
        result = host.secureSend(message, send_to_address,
                                 envelope_from, subject=subject,
                                 subtype=subtype, charset=encoding,
                                 debug=False, From=send_from_address)        


    def getTranslatedCategories(self, domain='osha'):
        """ returns a list of tuples, that contain key and title of Categories (Subject)
        ordered by Title """
        IGNORE = [ 'provider' ]
        pc = getToolByName(self.context, 'portal_catalog')
        plt = getToolByName(self.context, 'portal_languages')
        lang = plt.getPreferredLanguage()
        usedSubjects = pc.uniqueValuesFor('Subject')
        translate = getTranslationService().translate
        subjects = list()
        for s in usedSubjects:
            if s in IGNORE:
                continue
            subjects.append((s, 
                      translate(target_language=lang, msgid=s, default=s, context=self.context, domain=domain))
                     )
        subjects.sort(lambda x,y: cmp(x[1], y[1]))
        
        return subjects
        
        
    def getGermanNetwork(self):
        """ returns the sites from the European Network """
        return GERMAN_NETWORK
        
    def getEuropeanNetwork(self):
        """ returns the sites from the European Network """
        return EUROPEAN_NETWORK
    
    def getInternationalNetwork(self):
        """ returns the sites from the European Network """
        return INTERNATIONAL_NETWORK        

#translate(target_language='en', msgid='gender', default='wrong', context=self.context, domain='osha')
import Acquisition
from time import time
from osha.theme.browser.interfaces import IOSHA
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.interface import implements, alsoProvides
from plone.memoize.instance import memoize
from plone.memoize import ram


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
        



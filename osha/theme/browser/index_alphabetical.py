import Acquisition, time
from plone.memoize import ram
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class IndexAlphabetical(BrowserView):
    """View for displaying the thesaurus by alphabet
    """
    template = ViewPageTemplateFile('templates/index_alphabetical.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)
        context = Acquisition.aq_inner(self.context)        
        
        portal_vocabularies = getToolByName(context, 'portal_vocabularies')
        portal_languages = getToolByName(context, 'portal_languages')
        
        self.lang = portal_languages.getPreferredLanguage()
        self.manager = portal_vocabularies.MultilingualThesaurus._getManager() 
        self.term_dict = self.manager.term_dict
        self.letter = str(self.request.get('letter', '')).upper()
        self.term_id = self.request.get('term_id', '')
        
        return self.template() 


    def _getInitials_cachekey(method, self):
        return ("thesaurusinitials", self.lang)    
        
    @ram.cache(_getInitials_cachekey)
    def getInitials(self):
        """ fetch the whole alphabet """
        initials = {}
        for term_id in self.term_dict.keys():   
            term = self.term_dict[term_id]
            caption = self.manager.getTermCaptionById(term_id, self.lang).strip()
            if len(caption)==0:
                continue
            initial = caption[0].upper()
            section = initials.get(initial, [])
            section.append((caption, term_id))
            initials[initial] = section
        return initials
        
    def getAlphabet(self):
        """ fetch the whole alphabet """
        
        self.initials = self.getInitials()            
        alphabet = self.initials.keys()
        alphabet.sort()
        self.alphabet = alphabet
        return alphabet

        
    def resultsByLetter(self, letter=None):
        """ returns the sorted resultmap by letter based on the search above """
        #self._fetchResults()
        
        if letter is None:
            letter = self.getLetter()
        if letter == '':
            return [[], {}]
        
        section = self.initials.get(letter, [])    
        section.sort()
        return section

        
        
    def resultsByTermId(self, letter=None, term_id=None):
        """ returns the results sorted by ? based on letter and term_id
        """
        if letter is None:
            letter = self.getLetter()
        if letter == '':
            return []

        if term_id is None:
            term_id = self.getTerm_id()
        if term_id == '':
            return []

        resmap = self.captions.get(letter, {})        
        results = resmap.get(self.getCaptionById(term_id), [])
        return results
        
        
    def getSubject(self):
        return self.Subject

    def getLetter(self):
        return self.letter

    def getTerm_id(self):
        return self.term_id

    def getCaptionById(self, term_id):
        return self.manager.getTermCaptionById(term_id, self.lang)

    def getIdByCaption(self, caption):
        return self.caption_termid.get(caption, '')        
        
        
    def _searchCatalogForTerm_cachekey(method, self, term_id):
        return ("termresults", term_id)    
        
    @ram.cache(_searchCatalogForTerm_cachekey)
    def _searchCatalogForTerm(self, term_id):
        """ search the catalog for all items on a subject 
            this is to be cached 
        """
        start = time.time()
        context = Acquisition.aq_inner(self.context)        
        portal_catalog = getToolByName(context, 'portal_catalog')

        query = {'multilingual_thesaurus': term_id,
                 'Language': '', 
                 'review_state': 'published'
                }
        results = portal_catalog(query)                
        stop = time.time() 
        print "SearchTerm %s time is %s" % (self.term_id, stop-start)
        return len(results)
        
    def getTerm(self):
        portal_languages = getToolByName(self.context, 'portal_languages')
        langinfo = portal_languages.getAvailableLanguageInformation()

        term_id = self.term_id
        TERM = self.manager.getTermById(term_id)
        
        caption = self.manager.getTermCaptionById(term_id, self.lang)
        term = dict(id=self.term_id, Title=caption)

        results = self._searchCatalogForTerm(self.term_id)
        term['numEntries'] = results

        getC = self.manager.getTermCaptionById
        getI = self.manager.getTermIdentifier
        children = []
        for child in TERM.getchildren():
            if child.tag == '{http://www.imsglobal.org/xsd/imsvdex_v1p0}term':
                id = getI(child)
                caption = getC(id)
                children.append(dict(Title=caption, 
                         id=id, 
                         letter=caption[0],
                         numEntries=self._searchCatalogForTerm(id))) 

        term['childlist'] = children
        
        captions = self.manager.getTermCaption(TERM, lang='*')
        langs = captions.keys()
        langs.sort()
        translations = []
        for lang in langs:
            translations.append((captions[lang], lang, langinfo[lang]['native']))
        
        term['translations'] = translations        
        
        return term
        
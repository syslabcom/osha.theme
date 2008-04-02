import Acquisition, time
from plone.memoize import ram
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class IndexAtoZView(BrowserView):
    """View for displaying the publications overview page at /xx/publications
    """
    template = ViewPageTemplateFile('templates/atoz.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)
        context = Acquisition.aq_inner(self.context)        
        
        portal_vocabularies = getToolByName(context, 'portal_vocabularies')
        portal_languages = getToolByName(context, 'portal_languages')
        
        self.lang = portal_languages.getPreferredLanguage()
        self.manager = portal_vocabularies.MultilingualThesaurus._getManager() 
        self.term_dict = self.manager.term_dict
        self.Subject = self.request.get('Subject', context.getProperty('keyword', None))
        self.letter = self.request.get('letter', '').upper()
        self.term_id = self.request.get('term_id', '')
                
        return self.template() 
        
        
    def getAlphabet(self):
        """ fetch the whole alphabet """
        
        initials = {}
        for term_id in self.term_dict.keys():   
            caption = self.manager.getTermCaptionById(term_id, self.lang).strip()
            if len(caption)==0:
                continue
            initial = caption[0].upper()
            section = initials.get(initial, [])
            section.append(caption)
            initials[initial] = section
            
        self.initials = initials
        alphabet = initials.keys()
        alphabet.sort()
        self.alphabet = alphabet
        return alphabet

    def _searchCatalog_cachekey(method, self):
        return ("published_by_subject_alllanguages", self.Subject)    
        
    @ram.cache(_searchCatalog_cachekey)
    def _searchCatalog(self):
        """ search the catalog for all items on a subject 
            this is to be cached 
        """
        start = time.time()

        context = Acquisition.aq_inner(self.context)        
        portal_catalog = getToolByName(context, 'portal_catalog')

        query = {'Language': '', 
                 'Subject': self.Subject, 
                 'review_state': 'published'
                }
        results = portal_catalog(query)                
        stop = time.time()
        print "Catalog time is %s" % (stop-start)
        # The brain objects fetch the values potentially lazy only if needed. 
        # This may be bad for caching and seems to result in the hard to debug 
        # ConnectionStateError: Shouldn't load state for 0x3768d0 when the connection is closed error. 
        # I therefore copy the results over into a static datastructure.
        sres = []
        schema = portal_catalog.schema()
        for result in results:
            staticbrain = {}
            for key in schema:
                staticbrain[key] = result[key]
            staticbrain['getURL'] = result.getURL()
            staticbrain['getPath'] = result.getPath()
            
            sres.append(staticbrain)
            
        return sres
        
        
    def resultsByKeyword(self):
        """ search all objects which are categorized on given Subject
            and order them by alphabetical thesaurus term 
            E.g.
                {'A': [brain, brain]}
        """
        start = time.time()
                                
        results = self._searchCatalog()
        
        caption_termid = {}
        captions = {}
        for result in results:
            term_ids = result['getMTSubject'] or []
            for term_id in term_ids:
                caption = self.manager.getTermCaptionById(term_id, self.lang)
                caption_termid[caption] = term_id
                if not caption or len(caption)==0:
                    print "Caption error", caption
                    continue
                initial = caption[0].upper()
                section = captions.get(initial, {})
                captionmap = section.get(caption, [])
                captionmap.append(result)
                section[caption] = captionmap
                captions[initial] = section                
                
        self.captions = captions
        self.caption_termid = caption_termid

        initials = self.captions.keys()
        initials.sort()
        if not self.letter:
            self.letter = initials[0]
            
        stop = time.time()
        print "search duration %s secs" % (stop-start)
        return captions
        

        
    def resultsByLetter(self, letter=None):
        """ returns the sorted resultmap by letter based on the search above """
        if letter is None:
            letter = self.getLetter()
        if letter == '':
            return [[], {}]
            
        results = self.captions.get(letter, {})
        reskeys = results.keys()
        reskeys.sort()
        return (reskeys, results)
        
        
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
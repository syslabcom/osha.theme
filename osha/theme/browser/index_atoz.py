import Acquisition, time
from plone.memoize.view import memoize
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
        lang = portal_languages.getPreferredLanguage()
        self.lang = lang
        thesaurus = portal_vocabularies.MultilingualThesaurus
        manager = thesaurus._getManager()
        self.manager = manager 
        term_dict = manager.term_dict
        self.term_dict = term_dict
                
        return self.template() 
        
    #@memoize
    def getAlphabet(self):
        start = time.time()
        context = Acquisition.aq_inner(self.context)        

        initials = {}
        for term_id in self.term_dict.keys():   
            caption = self.manager.getTermCaptionById(term_id, self.lang).strip()
            if len(caption)==0:
                continue
            initial = caption[0].upper()
            section = initials.get(initial, [])
            section.append(caption)
            initials[initial] = section
            
        stop = time.time()
        self.duration_alphabet = stop-start
        self.initials = initials
        alphabet = initials.keys()
        alphabet.sort()
        self.alphabet = alphabet
        return alphabet
        
    def searchByKeyword(self, Subject=None):
        """ search all objects which are categorized on given Subject
            and order them by alphabetical thesaurus term 
            E.g.
                {'A': [brain, brain]}
        """
        start = time.time()
        context = Acquisition.aq_inner(self.context)        

        if Subject is None:
            Subject = context.getProperty('keyword', context.request.get('Subject', None))
        if Subject is None:
            return 
                        
        portal_catalog = getToolByName(context, 'portal_catalog')

        query = {'Language': '', 
                 'Subject': Subject, 
                 'review_state': 'published'
                }
        results = portal_catalog(query)                
        
        captions = {}
        for result in results:
            term_ids = result['getMTSubject'] or []
            for term_id in term_ids:
                caption = self.manager.getTermCaptionById(term_id, self.lang)
                if len(caption)==0:
                    continue
                initial = caption[0].upper()
                section = captions.get(initial, {})
                captionmap = section.get(caption, [])
                captionmap.append(result)
                section[caption] = captionmap
                captions[initial] = section                
                
        self.captions = captions
        
        stop = time.time()
        print "search duration %s secs" % (stop-start)
        return captions
        
    def getLetter(self):
        letter = self.context.request.get('letter', '').upper()
        return letter
        
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
        
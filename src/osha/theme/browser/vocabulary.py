from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
#from plone.memoize.forever import memoize
from plone.memoize import ram
from time import time

class VocabularyPathView(BrowserView):
    """View for calculating complete paths of hierarchical vocabulary entries
    """
    def __call__(self, fieldName=''):
        
        field = self.context.getField(fieldName)
        if not field:
            return []
#        import pdb; pdb.set_trace()
        termUID = field.getRaw(self.context)
        pvt = getToolByName(self.context, 'portal_vocabularies')
        VOCAB = getattr(field, 'vocabulary', None)
        if VOCAB is None:
            return []
        vd = VOCAB.getVocabularyDict(self.context)

        parents_map = dict()
        # list of current parents
        self.cp = list()
        
        def _recurseDict_cachekey(method, vocab_dict, level):
            return (vocab_dict.keys())

#        @ram.cache(_recurseDict_cachekey)
#        @ram.cache(lambda *args: time() // (60 * 60))
        def recurseDict(vocab_dict, level):
            for k in vocab_dict.keys():
                if level==0: 
                    self.cp = list()
                else:
                    self.cp = self.cp[:level]
                    parents_map[k] = [x for x in self.cp]
                vd = vocab_dict[k][1]
                if vd:
                    self.cp.append(k)
                    recurseDict(vd, level+1)
        recurseDict(vd, 0)

        res = set()
        for term in termUID:
            res.update(parents_map.get(term, []) + [term])

        return list(res)

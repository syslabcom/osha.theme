from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
#from plone.memoize.forever import memoize
from plone.memoize import ram
from time import time


def get_vocabulary_path(obj, fieldName=''):
    field = obj.getField(fieldName)
    if not field:
        return []
    termUID = field.getRaw(obj)
    pvt = getToolByName(obj, 'portal_vocabularies')
    VOCAB = getattr(field, 'vocabulary', None)
    if VOCAB is None:
        return []
    vd = VOCAB.getVocabularyDict(obj)

    parents_map = dict()
    # list of current parents
    global cp 
    cp = list()
    
    def _recurseDict_cachekey(method, vocab_dict, level):
        return (vocab_dict.keys())

#    @ram.cache(_recurseDict_cachekey)
#    @ram.cache(lambda *args: time() // (60 * 60))
    def recurseDict(vocab_dict, level):
        global cp
        for k in vocab_dict.keys():
            if level==0: 
                cp = list()
            else:
                cp = cp[:level]
                parents_map[k] = [x for x in cp]
            vd = vocab_dict[k][1]
            if vd:
                cp.append(k)
                recurseDict(vd, level+1)
    recurseDict(vd, 0)

    res = set()
    for term in termUID:
        res.update(parents_map.get(term, []) + [term])

    return list(res)


class VocabularyPathView(BrowserView):
    """View for calculating complete paths of hierarchical vocabulary entries
    """
    def __call__(self, fieldName=''):
       return get_vocabulary_path(self.context, fieldName)

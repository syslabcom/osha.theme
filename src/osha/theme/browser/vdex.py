from collective.dynatree.utils import dict2dynatree
from z3c.json.converter import JSONWriter
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName


class VDEXAsJson(object):

    def __init__(self, context, request):
        self.request = request
        self.context = context

    def __call__(self, vdex):
        tool = getToolByName(self.context, 'portal_vocabularies')
        vocab_dict = tool[vdex].getVocabularyDict(self.context)
        if vdex == 'NACE':
            showKey = True
        else:
            showKey = False

        transformed_dict = dict2dynatree(vocab_dict, [], False, showKey)
        return JSONWriter().write(transformed_dict)


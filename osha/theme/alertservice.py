from zope.interface import implements
from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.search import ISearchSchema
from Products.Archetypes.utils import DisplayList

from slc.alertservice import AlertMessageFactory as _

from slc.alertservice.interfaces import ISubjectGetter



class SubjectGetter(object):
    implements(ISubjectGetter)

    def __call__(self, context):
        pc = getToolByName(context, 'portal_catalog')
        pvt = getToolByName(context, 'portal_vocabularies', '')
        VOCAB = getattr(pvt, 'Subcategory', '')
        vd = VOCAB.getVocabularyDict(context)
        vocab_keys = vd.keys()
        subjects = pc.uniqueValuesFor('Subject')

        # get translation of subject from the vocabulary Subcategory
        DL = DisplayList()
        for subj in subjects:
            if subj in vocab_keys:
                trans = vd[subj][0] or subj
                DL.add(subj, trans)
        return DL

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import DisplayList

from slc.alertservice.interfaces import ISubjectGetter

from osha.theme import OSHAMessageFactory as _

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


class TypesGetter(object):

    def __call__(self, context):
        # do some hardcoding...
        seach_types = [ ('OSH_Link', _(u'OSH Link'))
                  , ('News Item', _(u'News'))
                  , ('Event', _(u'Event'))
                  , ('Publication', _(u'Publication'))
                  , ('CaseStudy', _(u'Case Study'))
                  ]
        DL = DisplayList()
        for st in seach_types:
            DL.add(st[0], st[1])

        return DL

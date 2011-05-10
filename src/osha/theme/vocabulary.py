from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from zope.app.component.hooks import getSite
from Products.CMFCore.utils import getToolByName
from plone.app.vocabularies.types import BAD_TYPES 
from Products.PluginIndexes.FieldIndex.FieldIndex import FieldIndex
from Products.PluginIndexes.DateIndex.DateIndex import DateIndex

BAD_TYPES = list(BAD_TYPES) + [
        'HelpCenterTutorialPage', 
        'HelpCenterReferenceManualPage',
        'HelpCenterLinkFolder'
        ]

class FriendlyTypesVocabulary(object):
    """ plone.app.vocbulary's ReallyUserFriendlyTypesVocabulary is not sorted 
        alphabetically.
        
        This vocabulary provides a sorted version.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        ttool = getToolByName(context, 'portal_types', None)
        if ttool is None:
            return None
        sorted_types = [
            (ttool[t].Title(), t) for t in ttool.listContentTypes() \
            if t not in BAD_TYPES
            ]
        sorted_types.sort()
        items = [ SimpleTerm(t[1], t[1], t[0]) for t in sorted_types]
        return SimpleVocabulary(items)

FriendlyTypesVocabulary = FriendlyTypesVocabulary()

class SubjectValuesVocabulary(object):
    """ Vocabulary factory returning all available index values for the
        'Subject' index.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        catalog  = getToolByName(site, 'portal_catalog')
        items = []
        for value in catalog.uniqueValuesFor('Subject'):
            items.append(SimpleTerm(value, value, value))

        return SimpleVocabulary(items)

SubjectValuesVocabulary = SubjectValuesVocabulary()

class SortableIndexesVocabulary(object):
    """ Vocabulary factory returning all available index values for the
        'Subject' index.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        items = []
        catalog  = getToolByName(site, 'portal_catalog')
        indexes = catalog._catalog.indexes
        for index in indexes:
            if type(indexes[index]) in (DateIndex, FieldIndex):
                items.append(SimpleTerm(index, index, index))
                
        return SimpleVocabulary(items)

SortableIndexesVocabulary = SortableIndexesVocabulary()

class SinToolKeyVocabulary(object):
    """Vocabulary factory returning all available keys in CMFSin's 
       sin_tool.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        sin = getToolByName(site, 'sin_tool')
        items = []
        for c in sin.Channels():
            items.append(SimpleTerm(c.id, c.id, c.id))

        return SimpleVocabulary(items)

SinToolKeyVocabulary = SinToolKeyVocabulary()

class PressContactVocabulary(object):
    """Vocabulary returning all the PressContacts in the catalog
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        cat = getToolByName(site, 'portal_catalog')
        items = []
        for c in cat(portal_type='PressContact'):
            items.append(SimpleTerm(c.id, c.getPath(), c.pretty_title_or_id))

        return SimpleVocabulary(items)

PressContactVocabulary = PressContactVocabulary()



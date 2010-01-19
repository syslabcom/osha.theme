from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from zope.app.component.hooks import getSite

from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.interfaces._vocabulary import IVocabulary
from Products.CMFCore.utils import getToolByName


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



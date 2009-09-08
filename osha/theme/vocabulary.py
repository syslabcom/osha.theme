import re 

from zope.app.component.hooks import getSite
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

from Products.CMFCore.utils import getToolByName

from slc.clicksearch.interfaces import IClickSearchConfiguration

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
    """Vocabulary factory returning all available keys in CMFSin's 
       sin_tool.
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

from Products.Archetypes.interfaces._vocabulary import IVocabulary
from Products.Archetypes.atapi import DisplayList

class AnnotatableLinkListVocabulary(object):
    """Vocabulary factory returning Section names for the AnnotatableLinkList Mechanism in the Document
    """
    implements(IVocabulary)

    def getDisplayList(self, context=None):
        """ """
        site = getSite()
        # perhaps check context for some settings, otherwise return a default
        return DisplayList([("simple1", "SimpleDesc1"), ("simple2", "SimpleDesc2")])

    def getVocabularyDict(self, instance=None):
        """ """
        pass

    def isFlat(self):
        """ returns true if the underlying vocabulary is flat, otherwise
            if its hierachical (tree-like) it returns false.
        """
        pass

    def showLeafsOnly(self):
        """ returns true for flat vocabularies. In hierachical (tree-like)
            vocabularies it defines if only leafs should be displayed, or
            knots and leafs.
        """
        pass

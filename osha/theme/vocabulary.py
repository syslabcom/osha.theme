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
            items.append(SimpleTerm(c.id, c.id, c.pretty_title_or_id))

        return SimpleVocabulary(items)

PressContactVocabulary = PressContactVocabulary()



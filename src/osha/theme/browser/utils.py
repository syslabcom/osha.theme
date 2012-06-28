from Products.LinguaPlone.catalog import languageFilter
from collective.solr.flare import PloneFlare
from collective.solr.interfaces import ISearch
from collective.solr.utils import prepareData
from zope.component import queryUtility

def search_solr(query, **params):
    search = queryUtility(ISearch)
    dummy = {}
    languageFilter(dummy)
    prepareData(dummy) # this replaces '' with 'any'
    langquery = 'Language:(%s)' % ' OR '.join(dummy['Language'])
    query = '(%s) AND %s' % (query, langquery)
    response = search(query, **params)
    results = response.results()
    for idx, flare in enumerate(results):
        results[idx] = PloneFlare(flare)
    return response

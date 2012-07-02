from Products.LinguaPlone.catalog import languageFilter
from collective.solr.flare import PloneFlare
from collective.solr.interfaces import ISearch
from collective.solr.utils import prepareData
from collective.solr.utils import padResults
from zope.component import queryUtility
from zope.component.hooks import getSite

def search_solr(query, request=None, **params):
    search = queryUtility(ISearch)
    dummy = {}
    languageFilter(dummy)
    prepareData(dummy) # this replaces '' with 'any'
    langquery = 'Language:(%s)' % ' OR '.join(dummy['Language'])
    query = '(%s) AND %s' % (query, langquery)
    response = search(query, **params)
    if request is None:
        request = getSite().REQUEST
    response.request = request
    results = response.results()
    for idx, flare in enumerate(results):
        results[idx] = PloneFlare(flare, request=request)
    padResults(results, **params)           # pad the batch
    return response

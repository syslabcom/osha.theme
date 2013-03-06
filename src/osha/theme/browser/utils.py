from collective.solr.flare import PloneFlare
from collective.solr.interfaces import ISearch
from collective.solr.utils import prepareData
from collective.solr.utils import padResults
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.LinguaPlone.catalog import languageFilter
from zope.component import queryUtility
from zope.component.hooks import getSite


def search_solr(query, request=None, **params):
    search = queryUtility(ISearch)
    dummy = {}
    languageFilter(dummy)
    prepareData(dummy)  # this replaces '' with 'any'
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


class EnableJSView(BrowserView):
    """View for enabling/disabling javascript files in portal_javascripts
    (e.g. jquery.highlighsearchterms.js) to prevent js errors and long
    loading times.
    """
    def __call__(self):
        """Returns True if context has default view selected as the active
        layout.
        """
        portal_types = getToolByName(self.context, 'portal_types')
        portal_type = getattr(self.context, 'portal_type', None)

        if portal_type:
            default_view = portal_types[portal_type].default_view
            if self.context.getLayout() == default_view:
                return True
        return False

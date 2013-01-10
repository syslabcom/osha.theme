import Acquisition
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

from collective.solr.mangler import iso8601date
from osha.theme.browser.dbfilter import DBFilterView

class WorklistView(DBFilterView):
    """View for displaying the worklist (filter plus result list)
    """

    def __call__(self):
        self.request.set('disable_border', True)

        return self.index()

    def getName(self):
        return self.__name__

    def search_types(self):
        """ Returns a list of translated search types to select from.
            This method is overwritten from dbfilter to provide a default
            list of types, so that all are selected initially.
        """
        context = Acquisition.aq_inner(self.context)

        default = [
                'OSH_Link', 'RALink', 'CaseStudy',
                'Provider', 'Publication', 'HelpCenterFAQ',
                'Directive', 'Modification', 'Amendment',
                'Note', 'Proposal'
                ]

        local_portal_types = context.getProperty('search_portal_types', default)
        search_portal_types = self.request.get('search_portal_types', local_portal_types)
        if not search_portal_types:
            search_portal_types = default

        TYPES = [
            ('Useful Link', 'OSH_Link', 'OSH_Link' in search_portal_types) ,
            ('Risk Assessment Tool', 'RALink', 'RALink' in search_portal_types) ,
            ('Case Study', 'CaseStudy', 'CaseStudy' in search_portal_types) ,
            ('Provider', 'Provider', 'Provider' in search_portal_types) ,
            ('Publication', 'Publication', 'Publication' in search_portal_types) ,
            ('Frequently Asked Question (FAQ)', 'HelpCenterFAQ', 'HelpCenterFAQ' in search_portal_types) ,
            ('Legislation Directive', 'Directive', 'Directive' in search_portal_types),
            ('Legislation Modification', 'Modification', 'Modification' in search_portal_types),
            ('Legislation Amendment', 'Amendment', 'Amendment' in search_portal_types),
            ('Legislation Note', 'Note', 'Note' in search_portal_types),
            ('Legislation Proposal', 'Proposal', 'Proposal' in search_portal_types)
            ]
        return TYPES


    def buildQuery(self):
        """ Build the query based on the request """
        context = Acquisition.aq_inner(self.context)

        queries = [self.search_portal_types()]

        local_keyword = context.getProperty('keyword', '')
        keywords = self.request.get('keywords', local_keyword)
        if keywords:
            queries.append('Subject:(%s)' % ' OR '.join(keywords))
            #query.update({'Subject':keywords})

        nace = list(self.request.get('nace', ''))
        if '' in nace:
            nace.remove('')
        if nace:
            queries.append('nace:(%s)' % ' OR '.join(nace))
            #query.update({'nace':nace})

        multilingual_thesaurus = list(self.request.get('multilingual_thesaurus', ''))
        if '' in multilingual_thesaurus:
            multilingual_thesaurus.remove('')
        if multilingual_thesaurus:
            queries.append('multilingual_thesaurus:(%s)' % ' OR '.join(multilingual_thesaurus))
            #query.update({'multilingual_thesaurus':multilingual_thesaurus})

        getRemoteLanguage = [x for x in self.request.get('getRemoteLanguage', [])]
        if getRemoteLanguage:
            if not isinstance(getRemoteLanguage, list):
                getRemoteLanguage = [getRemoteLanguage]
            if '' in getRemoteLanguage:
                getRemoteLanguage.remove('')
                getRemoteLanguage.append('any')
            queries.append('getRemoteLanguage:(%s)' % ' OR '.join(getRemoteLanguage))
            #query.update({'getRemoteLanguage':getRemoteLanguage})

        country = self.request.get('country', '')
        if country:
            queries.append('country:(%s)' % ' OR '.join(country))
            #query.update({'country':country})

        SearchableText = self.request.get('SearchableText', '')
        if SearchableText != '':
            queries.append('SearchableText:"%s"' % SearchableText)
            #query.update({'SearchableText': {'query': SearchableText, 'ranking_maxhits': 10000 }})

        Creator = [x for x in self.request.get('Creator', [])]
        if Creator:
            if not isinstance(Creator, list):
                Creator = [Creator]
            if '' in Creator:
                Creator.remove('')
            queries.append('Creator:(%s)' % ' OR '.join(Creator))
            #query.update(dict(Creator=Creator))

        subcategory = list(self.request.get('subcategory', ''))
        if '' in subcategory:
            subcategory.remove('')
        if subcategory:
            queries.append('subcategory:(%s)' % ' OR '.join(['"%s"' % s for s in subcategory]))
            #query.update({'subcategory':subcategory})

        getRemoteUrl = self.request.get('getRemoteUrl', '')
        if getRemoteUrl:
            queries.append('getRemoteUrl:%s' % getRemoteUrl)
            #query.update(dict(getRemoteUrl=getRemoteUrl))

        review_state = self.request.get('review_state', ['private', 'published', 'to_amend', 'pending', 'checked'])
        if review_state:
            queries.append('review_state:(%s)' % ' OR '.join(review_state))

        modified_year = self.request.get('modified_year', '')
        modified_month = self.request.get('modified_month', '')
        modified_day = self.request.get('modified_day', '')
        modified_mode = self.request.get('modified_mode', '')
        mdr = self.request.get('modified_days_range', 0)

        if modified_year and modified_month:
            if not modified_day:
                modified_day = 1
            searchdate = DateTime('%d/%d/%d' % (modified_year, modified_month, modified_day))
            if modified_mode=='before':
                queries.append('modified:[* TO %s]' % iso8601date(searchdate))
            elif modified_mode=='after':
                queries.append('modified:[%s TO *]' % iso8601date(searchdate))
            elif modified_mode=='range':
                queries.append('modified:[%(from)s TO %(to)s]' % \
                        {'from': iso8601date(searchdate - mdr), 
                         'to': iso8601date(searchdate + mdr)})

        lang = getToolByName(self.context, 'portal_languages').getPreferredLanguage()
        queries.append('Language:(%s OR any)' % lang)

        query = ' AND '.join(queries)

        return query



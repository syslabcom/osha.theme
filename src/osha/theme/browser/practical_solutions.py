from Acquisition import aq_inner, aq_parent
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName

from osha.theme.browser.dbfilter import DBFilterView
from osha.theme.browser.utils import search_solr


class PracticalSolutionsView(DBFilterView):
    """ View Class for the Practical Solutions page.

        Provides a link to each section based on the folder title.
        If there is an image called "section-image.png" in the folder
        it will be used too.
        """

    gpawards = ''
    intro = ''
    has_section_details = False
    sections = ['useful-links',
                'risk-assessment-tools',
                'case-studies',
                'providers',
                'faqs']

    def __call__(self):
        self.request.set('disable_border', True)

        intro = getattr(self.context, 'introduction_html', None)
        if intro is None:
            self.intro = ''
        else:
            self.intro = intro.CookedBody()

        gpaward = getattr(self.context, 'good_practice_awards_html', None)
        if gpaward is None:
            self.gpaward = ''
        else:
            self.gpaward = gpaward.CookedBody()

        return self.index()


    def search_portal_types(self):
        context = self.context
        preflang = getToolByName(self.context,
                                 'portal_languages').getPreferredLanguage()
        search_portal_types = [ "OSH_Link", "RALink", "CaseStudy", "Provider", "HelpCenterFAQ"]
        query = 'portal_type:(%(portal_type)s) AND Language:(%(Language)s) AND review_state:published' % \
                {'portal_type': ' OR '.join(search_portal_types),
                 'Language': ' OR '.join([preflang, 'any']),}
        return query

    def getSectionDetails(self):
        """ Return a path to an image and a title for each of the five
            Practical Solutions sections.
            """
        context = self.context
        section_details = {}

        for section in self.sections:
            if section in context.objectIds():
                section_details[section] = {}
                # The title is taken from the local version
                section_details[section]["title"] = context[section].Title()
                canonical_section = context.getCanonical()[section]
                # The image is taken from the canonical version
                if "section-image.png" in canonical_section.objectIds():
                    section_details[section]["section_image_src"] = \
                        canonical_section["section-image.png"].absolute_url()
                self.has_section_details = True
        return section_details


class PracticalSolutionView(DBFilterView):
    """View for displaying one of the practical solution sections.

    The section heading, image and search parameters (portal_type) are derived
    from the parent folder.

    The Title of the parent folder is used as a caption under the image for the
    current section (to be consistent with the PracticalSolutionsView).
    If there is an image in that folder called 'section-image.png' it will be
    used too.
    The portal-type to search for is derived from the id of the parent
    folder.
    """

    portal_types_map = {
            "useful-links":"OSH_Link",
            "risk-assessment-tools":"RALink",
            "case-studies":"CaseStudy",
            "providers":"Provider",
            "faqs":"HelpCenterFAQ",
            "publications": "Publication"
            }

    def __call__(self):
        self.request.set('disable_border', True)
        return self.index()

    def has_section_image(self):
        """ Check if an image called section-image.png exists in the folder """
        context = self.context
        parent = aq_parent(aq_inner(context))
        return "section-image.png" in parent.objectIds()

    def get_i18n_database_search_heading(self):
        """ Method to get the localised heading for the database
        search box.
        """
        context = self.context
        parent = aq_parent(aq_inner(context))
        section_id = parent.getId()
        preflang = getToolByName(self.context,
                                 'portal_languages').getPreferredLanguage()
        # convert "useful-links" to "heading_useful_links"
        msgid = "heading_search_%s" % section_id.replace("-", "_")
        heading  = translate(domain="osha",
                                 msgid=msgid,
                                 context=context,
                                 target_language=preflang,
                                 default=parent.Title())
        return heading

    def get_keyword(self):
        """ Return the first value from keywords/request or an empty string
        """
        keywords = self.request.get("keywords", "")
        keyword = ""
        if keywords:
            keyword = keywords[0]
        return keyword

    def get_search_portal_type(self):
        """ Work out the relevant search_portal_types value from the
        query string or the parent id.
        """
        context = self.context
        parent = aq_parent(aq_inner(context))
        local_search_portal_type = []
        if self.portal_types_map.has_key(parent.id):
            local_search_portal_type = self.portal_types_map[parent.id]
        search_portal_types = self.request.get('search_portal_types',
                                               local_search_portal_type)
        return search_portal_types

    def translate(self, msgid):
        context = self.context
        preflang = getToolByName(self.context,
                                 'portal_languages').getPreferredLanguage()
        return translate(domain="osha",
                                     msgid=msgid,
                                     context=context,
                                     target_language=preflang)

    def search_types(self):
        """ Return a list of translated search types to select
        from. This overrides the DBFilterView method to remove
        Publication and select the database using
        get_search_portal_type. """

        search_portal_types = self.get_search_portal_type()
        # if all are turned off, turn them all on. Searching for
        # nothing makes no sense.
        if not search_portal_types:
            search_portal_types = ['OSH_Link', 'RALink',
                                   'CaseStudy', 'Provider',
                                   'HelpCenterFAQ']
        TYPES = [
            (self.translate("label_useful_links"), 'OSH_Link',
             'OSH_Link' in search_portal_types) ,
            (self.translate("label_risk_assessment_tools"), 'RALink',
             'RALink' in search_portal_types) ,
            (self.translate("label_case_studies"), 'CaseStudy',
             'CaseStudy' in search_portal_types) ,
            (self.translate("label_providers"), 'Provider',
             'Provider' in search_portal_types) ,
            (self.translate("FAQ"), 'HelpCenterFAQ',
             'HelpCenterFAQ' in search_portal_types) ,
                ]

        return TYPES

    def search_portal_types(self):
        """ Publications are files with the IPublicationEnhanced
        interface """
        context = self.context
        search_portal_types = self.get_search_portal_type()
        query = None
        if 'Publication' in search_portal_types:
            query = '(portal_type:File AND object_provides:slc.publications.interfaces.IPublicationEnhanced)'
            search_portal_types.remove('Publication')
            query = ' OR '.join([query, 'portal_type:(%s)' % ' OR '.join(search_portal_types)])
        else:
            query = 'portal_type:(%s)' % ' OR '.join(search_portal_types)
        query = '(%s) AND review_state:published' % query
        return query

    def has_subcategory(self, subject=''):
        """ Do we have subcategory values for the given subject?
        """
        pvt = getToolByName(self.context, 'portal_vocabularies')
        vocab = getattr(pvt, 'Subcategory', None)
        if not vocab:
            return False
        return bool(vocab.getTermByKey(subject))

    def buildQuery(self):
        """ Build the query based on the request.
        Overriding this method from DBFilter because it treats an
        empty keywords:list as a value causing nothing to be returned
        """
        context = aq_inner(self.context)
        query = self.search_portal_types()

        # It is likely that this should be replaced by context.Subject()
        # this was the case with #3806
        local_keyword = context.getProperty('keyword', '')

        keywords = self.request.get('keywords', local_keyword)
        if keywords:
            if keywords !=  ['']:
                query = ' AND '.join([query, 'Subject:(%s)' % ' OR '.join(keywords)])

        nace = list(self.request.get('nace', ''))
        if '' in nace:
            nace.remove('')
        if nace:
            query = '%(query)s AND %(nace)s' % {'query': query, 'nace': 'nace:(%s)' % ' OR '.join(nace)}
            #query.update({'nace':nace})

        multilingual_thesaurus = list(self.request.get('multilingual_thesaurus', ''))
        if '' in multilingual_thesaurus:
            multilingual_thesaurus.remove('')
        if multilingual_thesaurus:
            query = '%(query)s AND %(mul_the)s' % \
                    {'query': query, 'mul_the': 'multilingual_thesaurus:(%s)' % ' OR '.join(multilingual_thesaurus)}
            #query.update({'multilingual_thesaurus':multilingual_thesaurus})

        preflang = getToolByName(self.context,
                                 'portal_languages').getPreferredLanguage()
        language = self.request.get('Language', preflang)
        # Important! Always include neutral! Neutral == relevant for ALL
        # languages!!!
        if language:
            query = '%(query)s AND Language:(%s)' % (query, ' OR '.join((language, 'any')))

        # don't handle remoteLanguage for FAQHelpcenter items
        spt = self.get_search_portal_type()
        faq_condition = type(spt) == list and 'HelpCenterFAQ' in spt or spt == 'HelpCenterFAQ'
        getRemoteLanguage = self.request.get('getRemoteLanguage',
                                             not faq_condition and preflang
                                             or '')
        if getRemoteLanguage:
            query = '%(query)s AND %(getRemoteLanguage)s' % {'query': query, 'getRemoteLanguage': 'getRemoteLanguage:(%s)' % ' OR '.join(getRemoteLanguage)}
            #query.update({'getRemoteLanguage':getRemoteLanguage})

        subcategory = self.request.get('subcategory', '')
        if subcategory:
            query = '%(query)s AND %(subcategory)s' % {'query': query, 'subcategory': 'subcategory:(%s)' % ' OR '.join(subcategory)}
            #query.update({'subcategory':subcategory})

        country = self.request.get('country', '')
        if country:
            query = '%(query)s AND %(country)s' % {'query': query, 'country': 'country:(%s)' % ' OR '.join(country)}
            #query.update({'country':country})

        SearchableText = self.request.get('SearchableText', '')
        if SearchableText != '':
            query = '%(query)s AND SearchableText:%(SearchableText)s' % {'query': query, 'SearchableText': SearchableText}
            #query.update({'SearchableText': {'query': SearchableText, 'ranking_maxhits': 10000 }})

        return query

    def get_link_to_english_results(self):
        """
        If the selected language is not English, then return a link to
        the equivalent search results in English
        """
        preflang = getToolByName(self.context,
                                 'portal_languages').getPreferredLanguage()
        url = ""
        if preflang != "en":
            solution = self.aq_parent.getCanonical().absolute_url()
            keywords = self.request.get("keywords", "")
            if keywords and keywords != [""]:
                keywords = keywords[0]
            url = "%s?keywords:list=%s#database_search"\
                  % (solution, keywords)
        return url

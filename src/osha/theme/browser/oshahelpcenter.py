from collective.solr.solr import SolrException
from ordereddict import OrderedDict
from osha.theme.portlets.navigation import getNavigationRoot
from Products.Five.browser import BrowserView
from zope.app.component.hooks import getSite

import logging

logger = logging.getLogger('osha.theme.browser.oshahelpcenter')


class OSHAHelpCenterView(BrowserView):
    """ support for HelpCenter templates """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        self.faq_form = self.request.form
        self.category = self.faq_form.get("category", "")
        self.portal = getSite()
        self.pc = self.portal.portal_catalog
        self.faqfolder = getattr(getNavigationRoot(self.context), 'faq', None)

        subcategory_vocab = self.portal.portal_vocabularies.Subcategory
        self.vocab_dict = subcategory_vocab.getVocabularyDict(self.context)
        return self.index()

    def getName(self):
        return self.__name__

    @property
    def get_faqs(self):
        """ Return a list of FAQ objects. """
        query = {}
        query["portal_type"] = "HelpCenterFAQ"

        searchable_text = self.faq_form.get("SearchableText", "")
        if searchable_text != "":
            query["SearchableText"] = searchable_text

        subcategory = self.faq_form.get("subcategory", "") or self.category
        if subcategory:
            query["subcategory"] = subcategory

        if searchable_text == subcategory == "":
            if self.faqfolder is not None:
                path = "/".join(self.faqfolder.getPhysicalPath())
                query["path"] = path + "/general-information"

        try:
            faq_brains = self.pc.searchResults(query)
            faqs = [i.getObject() for i in faq_brains]
        except SolrException:
            logger.exception('Error during solr search for string "%s"'
                             % searchable_text)
            faqs = []

        return faqs

    def _get_relevant_categories(self, faqs, vocab_dict):
        """We are only interested either in the categories at the top
        level or below the current category. We also only want
        categories which are being used."""
        if self.category:
            category_attr = "subcategory"
        else:
            category_attr = "Subject"
        possible_categories = vocab_dict.keys()

        faq_categories = set()
        for faq in faqs:
            for category in getattr(faq, category_attr):
                faq_categories.add(category)
        rlv_cats = faq_categories.intersection(possible_categories)
        # import pdb; pdb.set_trace()
        return rlv_cats

    def _sort_categories_by_title(self, categories, vocab_dict):
        """ Return a list of category ids, sorted by the title. The
        title of an item in a vocab_dict is the first element of the
        tuple. """
        category_titles = []
        for category in categories:
            title = vocab_dict[category][0]
            category_titles.append((category, title))
        sorted_categories = sorted(category_titles, key=lambda x: x[1])
        return [i[0] for i in sorted_categories]

    def _get_categories(self, faqs, vocab_dict):
        """ Return a sorted vocab_dict of relevant categories. """
        relevant_categories = self._get_relevant_categories(faqs, vocab_dict)

        sorted_categories = self._sort_categories_by_title(
            relevant_categories, vocab_dict)

        category_dict = OrderedDict()
        for category in sorted_categories:
            category_dict[category] = vocab_dict[category]

        return category_dict

    def get_categories(self):
        """ The "subcategory" field is not stored in the metadata but
        the top level "subcategory" is indexed as "Subject". We take
        advantage of this to get a list of all the top level
        "subcategory" values which are actually in use.
        """
        if self.category:
            return []
        faq_brains = self.pc.searchResults({"portal_type": "HelpCenterFAQ"})
        return self._get_categories(faq_brains, self.vocab_dict)

    def get_subcategories(self, category):
        """ Get a list of "subcategory" values from FAQ objects with
        the selected category
        """
        subcat_vocab_dict = category in self.vocab_dict and \
            self.vocab_dict[category][1] or None
        if not subcat_vocab_dict:
            return []

        faq_brains = self.pc.searchResults({"portal_type": "HelpCenterFAQ",
                                            "Subject": category})
        faqs = [i.getObject() for i in faq_brains]

        return self._get_categories(faqs, subcat_vocab_dict)

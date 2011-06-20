from zope.app.component.hooks import getSite
from ordereddict import OrderedDict
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class OSHAHelpCenterView(BrowserView):
    """ support for HelpCenter templates """

    template = ViewPageTemplateFile('templates/osha_help_center_view.pt')
    template.id = "osha_help_center_view"

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.faq_form = self.request.form
        self.category = self.faq_form.get("category", "")
        self.portal = getSite()
        self.pc = self.portal.portal_catalog
        self.faqs = self.get_faqs()

        subcategory_vocab = self.portal.portal_vocabularies.Subcategory
        self.vocab_dict = subcategory_vocab.getVocabularyDict(self.context)

    def __call__(self):
        return self.template()

    def get_faqs(self):
        """ Return a list of FAQ objects. """
        query = {}
        query["portal_type"] = "HelpCenterFAQ"

        searchable_text = self.faq_form.get("SearchableText", "")
        if searchable_text != "":
            query["SearchableText"] = searchable_text

        subcategory = self.faq_form.get("subcategory", "")  or self.category
        if subcategory:
            query["subcategory"] = subcategory

        if searchable_text == subcategory == "":
            path = "/".join(self.context.getPhysicalPath())
            query["path"] = path+"/general-information"

        faq_brains = self.pc.searchResults(query)
        faqs = [i.getObject() for i in faq_brains]
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
        return faq_categories.intersection(possible_categories)

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
        subcat_vocab_dict = self.vocab_dict[category][1]
        if not subcat_vocab_dict:
            return []

        faq_brains = self.pc.searchResults({"portal_type":"HelpCenterFAQ",
                                            "Subject":category})
        faqs = [i.getObject() for i in faq_brains]

        return self._get_categories(faqs, subcat_vocab_dict)

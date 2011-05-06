from zope.app.component.hooks import getSite

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class OSHAHelpCenterView(BrowserView):
    """ support for HelpCenter templates """

    template = ViewPageTemplateFile('templates/osha_help_center_view.pt')
    template.id = "osha_help_center_view"

    def __call__(self):
        return self.template()

    def get_vocab_dict(self):
        portal = getSite()
        pv = portal.portal_vocabularies
        vocab = pv.Subcategory
        return vocab.getVocabularyDict(self.context)

    def get_faqs_in_selected_category(self):
        portal = getSite()
        pc = portal.portal_catalog
        query = {}
        query["portal_type"] = "HelpCenterFAQ"

        form = self.request.form

        searchable_text = form.get("SearchableText", "")
        if searchable_text != "":
            query["SearchableText"] = searchable_text

        subcategory = form.get("subcategory", "") or form.get("category", "")
        if subcategory:
            query["subcategory"] = subcategory

        if searchable_text == subcategory == "":
            path = "/".join(self.context.getPhysicalPath())
            query["path"] = path+"/general-information"

        faqs = pc.searchResults(query)
        return faqs

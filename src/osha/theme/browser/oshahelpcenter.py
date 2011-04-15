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

    def get_subject_counts(self):
        """get the Subject/Subcategory for all FAQ objects in this area

        Since we get them all anyway, we might as well count the
        number of items in each category, also get the translation
        from the translation for Subject
        {'young_people': 21, 'disability': 27, ...} """
        portal = getSite()

        pc = portal.portal_catalog
        path = "/".join(self.context.getPhysicalPath())
        faqs = pc.searchResults({"portal_type":"HelpCenterFAQ",
                                 "path":path})

        subjects = {}
        for faq in faqs:
            for subject in faq.Subject:
                count = subjects.setdefault(subject, 0)
                subjects[subject] = count + 1
        return subjects

    def get_vocab_dict(self):
        portal = getSite()
        pv = portal.portal_vocabularies
        vocab = pv.Subcategory
        return vocab.getVocabularyDict(self.context)

    def get_subject_list(self):
        """get a list of Subjects/Subcategories

        Sorted by the translated term
        [{"title":"Accident Prevention",
          "key":"accident_prevention",
          "count": 10}, ...] """
        vocab_dict = self.get_vocab_dict()
        subjects = self.get_subject_counts()
        subject_list = []
        for subject in subjects:
            subject_list.append({"title":vocab_dict[subject][0],
                                 "key":subject,
                                 "count":subjects[subject]})
        return sorted(subject_list, key=lambda x: x["title"])

    def get_sub_subject_list(self, subject):
        """get a list of sub-subject from the vocabulary"""
        vocab_dict = self.get_vocab_dict()
        sub_subjects = vocab_dict[subject][1]
        sub_subject_list = []
        for sub_subject in sub_subjects:
            sub_subject_list.append({"title":sub_subjects[subject][0],
                                     "key":subject})


from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class PublicationsSearchView(BrowserView):
    """View for displaying the publications overview page at /xx/publications
    """
    template = ViewPageTemplateFile('templates/publicationsearch.pt')
    template.id = "publications-overview"
    
    def __call__(self):
        self.request.set('disable_border', True)

        return self.template() 

    def get_subject(self):
        subject = self.request.get('Subject', '')
        if subject == ['']:
            subject = ''
        #subject = [x.encode('utf-8') for x in subject]
        return subject

    def make_query(self):
        query = {'portal_type': 'File', 
                 'object_provides': 'slc.publications.interfaces.IPublicationEnhanced',
                 'sort_on': 'effective',
                 'sort_order':'reverse'}
        if self.get_subject():
            query.update({'Subject': self.get_subject()})
        
        st = self.request.get('SearchableText' '')
        if st:
            query.update({'SearchableText': st})
        return query
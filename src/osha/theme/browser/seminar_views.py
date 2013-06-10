from slc.seminarportal.browser.views import SeminarFolderView

from zope.interface import implements

import Acquisition
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName

class LanguageFallbackView(SeminarFolderView):
    """ View methods for the seminar folder view
    """

    def seminars(self):
        """ Return brains for SPSeminar objects in context
        """
        context = Acquisition.aq_inner(self.context)
        catalog = getToolByName(self.context, 'portal_catalog')
        if not IFolderish.providedBy(context):
            # We might be on a index_html
            folder = context.aq_parent
        else:
            folder = self.context

        query = {
            'portal_type': 'SPSeminar',
            'path': '/'.join(folder.getPhysicalPath()),
            'sort_on': 'start',
            'sort_order': 'reverse',
            }
        search_view = context.restrictedTraverse('@@language-fallback-search')
        return search_view.search(query)

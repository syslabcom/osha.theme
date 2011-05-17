import Acquisition
from DateTime import DateTime

from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

class ItemListingView(BrowserView):
    """" """

    def isAnonymous(self):
        """ """
        anonymous = getToolByName(self, 'portal_membership').isAnonymousUser()
        return anonymous

    def date(self, date=None):
        """Return the DateTime obj
        """
        return DateTime(date)

    def increment_date(self, date):
        return DateTime(date)+1

    def cropHtmlText(self, text, length, ellipsis='...'):
        """ First strip html, then crop """
        context = Acquisition.aq_inner(self.context)
        portal_transforms = getToolByName(context, 'portal_transforms')
        text = portal_transforms.convert('html_to_text', text).getData()
        return context.restrictedTraverse('@@plone').cropText(text, length, ellipsis)

    def items(self, portal_type=None):
        """ Return brains for objects (of portal_type) in current folder 
        """
        context = Acquisition.aq_inner(self.context)
        request = self.context.request
        catalog = getToolByName(self.context, 'portal_catalog')
        if not IFolderish.providedBy(context):
            # We might be on a index_html
            folder = context.aq_parent
        else:
            folder = self.context
        query = {
            'path':'/'.join(folder.getPhysicalPath()),
            'sort_on': 'created',
            'sort_order': 'reverse',
            }
        if portal_type is not None:
            query['portal_type'] = portal_type
        return catalog(query)


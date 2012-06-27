try:
    from Products.Collage.browser.existingitems import ExistingItemsView
    from Products.Collage.config import COLLAGE_TYPES
except:
    from Products.Collage.browser.column import ExistingItemsView, COLLAGE_TYPES
from Products.CMFPlone import utils as cmfutils
from urlparse import urljoin


class EnhancedExistingItemsView(ExistingItemsView):

    def portal_path(self):
        url_tool = cmfutils.getToolByName(self.context, 'portal_url')
        return '/'.join(url_tool.getPortalObject().getPhysicalPath() + ('',))

    def getItems(self):
#        import pdb; pdb.set_trace()
        SearchableText = self.request.get('SearchableText', '')
        path = self.request.get('path', '').strip()
        if path:
            path = path.replace('%2F', '/')
            if path[0]=='/': path = path[1:]
            abspath = urljoin(self.portal_path(), path)
        else:
            abspath = ''
        if SearchableText=='' and abspath=='':
            return list()
        langtool = cmfutils.getToolByName(self.context, 'portal_languages')
        prefLang = langtool.getPreferredLanguage()
        items = self.catalog(SearchableText=SearchableText,
                             Language=['', prefLang],
                             path=abspath,
                             sort_order='reverse',
                             sort_on='modified')
        # filter out collage content types
        items = [i for i in items if i.portal_type not in COLLAGE_TYPES]
    
        # limit count
        items = items[:self.request.get('count', 50)]
    
        # setup description cropping
        try:
            cropText = self.context.restrictedTraverse('@@plone').cropText
        except AttributeError:
            # BBB: Plone 2.5
            cropText = self.context.cropText
    
        props = cmfutils.getToolByName(self.context, 'portal_properties')
        site_properties = props.site_properties
        
        desc_length = getattr(site_properties, 'search_results_description_length', 25)
        desc_ellipsis = getattr(site_properties, 'ellipsis', '...')
        
        return [{'UID': obj.UID(),
                 'icon' : result.getIcon,
                 'title': result.Title,
                 'description': cropText(result.Description, desc_length, desc_ellipsis),
                 'type': result.Type,
                 'portal_type':  result.portal_type,
                 'modified': result.ModificationDate,
                 'published': result.EffectiveDate or ''} for (result, obj) in
                map(lambda result: (result, result.getObject()), items)]

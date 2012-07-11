from plone.app.portlets.portlets import navigation
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Acquisition import aq_base, aq_inner, aq_parent
from Products.CMFPlone import utils

class Renderer(navigation.Renderer):
    """Dynamically override standard header for navtree portlet"""
    
    _template = ViewPageTemplateFile('safestartnavigation.pt')
    recurse = ViewPageTemplateFile('safestartnavigation_recurse.pt')
    

    def root_item_class(self):
        context = aq_inner(self.context)
        root = self.getNavRoot()
        if (aq_base(root) is aq_base(context) or
                (aq_base(root) is aq_base(aq_parent(aq_inner(context))) and
                utils.isDefaultPage(context, self.request))):
            return 'active'
        else:
            return 'default'

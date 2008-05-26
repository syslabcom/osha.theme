import Acquisition
from time import time
from osha.theme.browser.interfaces import ILinguaToolsView
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.interface import implements, alsoProvides
from plone.memoize.instance import memoize
from plone.memoize import ram
from plone.portlets.constants import CONTEXT_CATEGORY, GROUP_CATEGORY, CONTENT_TYPE_CATEGORY
from plone.app.portlets.portlets import navigation, news, classic, events, search
from plone.app.portlets.utils import assignment_mapping_from_key
from zope.component import getMultiAdapter, getUtility
from plone.portlets.interfaces import IPortletManager, ILocalPortletAssignmentManager

class LinguaToolsView(BrowserView):
    implements(ILinguaToolsView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.portal_url = getToolByName(context, 'portal_url')
        self.portal_path = self.portal_url.getPortalPath()
        self.portal = self.portal_url.getPortalObject()
        self.portal_languages = getToolByName(context, 'portal_languages')
        self.langs = self.portal_languages.getSupportedLanguages()
        self.dynamic_path = self.portal_path + '/%s/' + "/".join(context.getPhysicalPath()[len(self.portal.getPhysicalPath())+1:])
        print self.dynamic_path
        
        
    def _forAllLangs(self, method, *args, **kw):
        """ helper method. Takes a method and executes it on all language versions of context """
        context = Acquisition.aq_inner(self.context)
        results = []
        for lang in self.langs:
            lpath = self.dynamic_path%lang
            base = context.restrictedTraverse(lpath, None)
            if base is None:
                continue
            res = method(base, *args, **kw)
            results.append("Exec: %s for %s" % (method.__name__, lang))
            if res:
                results += list(res)
                
        return results
    
    
    def blockPortlets(context, manager, CAT, status):
        """ Helper. Block the Portlets on a given context, manager, and Category """
        portletManager = getUtility(IPortletManager, name=manager)
        assignable = getMultiAdapter((context, portletManager,), ILocalPortletAssignmentManager)    
        assignable.setBlacklistStatus(CAT, status)
    
    
#    def blockPortletsButNavi(self):
#        """ changes for all campaign sites """
#        # Block the portlets
#        context = self
#        path = '/'.join(context.getPhysicalPath())
#        left = assignment_mapping_from_key(context, 'plone.leftcolumn', CONTEXT_CATEGORY, path)
#        right = assignment_mapping_from_key(context, 'plone.rightcolumn', CONTEXT_CATEGORY, path)
#        belowcontext = assignment_mapping_from_key(context, 'osha.belowcontent.portlets', CONTEXT_CATEGORY, path)
#    
#        for x in list(left.keys()):
#            del left[x]    
#    
#        for x in list(right.keys()):
#            del right[x]    
#    
#        for x in list(belowcontext.keys()):
#            del belowcontext[x]    
#    
#        _blockPortlets(context, 'plone.leftcolumn', CONTEXT_CATEGORY, True)
#        _blockPortlets(context, 'plone.rightcolumn', CONTEXT_CATEGORY, True)
#        _blockPortlets(context, 'osha.belowcontent.portlets', CONTEXT_CATEGORY, True)
#    
#        left['navtree'] = navigation.Assignment(topLevel=0)
#        
    
    
    def setExcludeFromNav(self, flag=True):
        """ Sets the Exclude From nav flag """
        def _setter(ob):
            ob.setExcludeFromNav(flag)
        self._forAllLangs(_setter)

    def setEnableNextPrevious(self, flag=True):
        """ Enables the Next-Previous Navigation Flag """
        def _setter(ob):
            ob.setNextPreviousEnabled(flag)
        self._forAllLangs(_setter)
        
    def setTitle(self, title):
        """ simply set the title to a given value. Very primitive! """
        def _setter(ob, title):
            ob.setTitle(title)
        self._forAllLangs(self.dynamic_path, _setter, title=title)
    
    def renamer(self, oldid, newid):
        """ rename one object within context from oldid to newid """
        def _setter(ob, oldid=oldid, newid=newid):
            if oldid in ob.objectIds():
                ob.manage_renameObjects([oldid], [newid])
        self._forAllLangs(_setter, oldid=oldid, newid=newid)
        
    def fixOrder(self, ORDER):
        """Move contents of a folter into order
            make sure the ordering of the folders is correct
        """
        plone_utils = getToolByName(self.context, 'plone_utils')

        def _orderIDs(base, ids=[]):
            """sorts the objects in base in the order given by ids"""
            ids.reverse()
            base_ids = base.objectIds()
            flag = 0
            if len(base_ids)>= len(ids) and base_ids[:len(ids)] == ids:
                return
            for id in ids:
                if id in base_ids:
                    flag = 1
                    base.moveObjectsToTop(id)
            if flag == 1: # only reindex if there is something to do
                plone_utils.reindexOnReorder(base)
        self._forAllLangs(_orderIDs, ids=ORDER)          
                
    def deleter(self, id):
        """ deletes an object with a given id from all language branches """
        def _setter(ob, id):
            if id in ob.objectIds():
                ob._delObject(id)
        self._forAllLangs(_setter, id=id)
        
    def propagatePortlets(self):
        """ propagates the portlet config from context to the language versions """
        context = Acquisition.aq_inner(self.context)
        path = "/".join(context.getPhysicalPath()) 
        left = assignment_mapping_from_key(context, 'plone.leftcolumn', CONTEXT_CATEGORY, path)
        right = assignment_mapping_from_key(context, 'plone.rightcolumn', CONTEXT_CATEGORY, path)
        belowcontext = assignment_mapping_from_key(context, 'osha.belowcontent.portlets', CONTEXT_CATEGORY, path)
        
        def _setter(ob, cleft, cright, cbelowcontext):   
            if ob.getCanonical() == ob:
                return
            if ob.portal_type == 'LinguaLink':
                return
            path = "/".join(ob.getPhysicalPath()) 
            left = assignment_mapping_from_key(ob, 'plone.leftcolumn', CONTEXT_CATEGORY, path)
            right = assignment_mapping_from_key(ob, 'plone.rightcolumn', CONTEXT_CATEGORY, path)
            belowcontext = assignment_mapping_from_key(ob, 'osha.belowcontent.portlets', CONTEXT_CATEGORY, path)
    
            for x in list(left.keys()):
                del left[x]
            for x in list(cleft.keys()):
                left[x] = cleft[x]                   
        
            for x in list(right.keys()):
                del right[x]    
            for x in list(cright.keys()):
                right[x] = cright[x]
        
            for x in list(belowcontext.keys()):
                del belowcontext[x]    
            for x in list(cbelowcontext.keys()):
                belowcontext[x] = cbelowcontext[x]

        self._forAllLangs(_setter, cleft=left, cright=right, cbelowcontext=belowcontext)
        
        

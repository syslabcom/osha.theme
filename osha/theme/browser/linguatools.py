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
from zope.event import notify
from zope.lifecycleevent import ObjectCopiedEvent
from zope.app.container.contained import ObjectMovedEvent
from zope.app.container.contained import notifyContainerModified
from OFS.event import ObjectWillBeMovedEvent
from OFS.event import ObjectClonedEvent
from Products.PloneLanguageTool.LanguageTool import LanguageTool
from p4a.subtyper.interfaces import ISubtyper

from Products.PlacelessTranslationService import getTranslationService

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
        if self.dynamic_path[-1]== "/":
            self.dynamic_path = self.dynamic_path[:-1]
        
    def _forAllLangs(self, method, *args, **kw):
        """ helper method. Takes a method and executes it on all language versions of context """
        context = Acquisition.aq_inner(self.context)
        results = []
        for lang in self.langs:
            results.append("Trying language: %s" % lang)
            lpath = self.dynamic_path%lang
            base = context.restrictedTraverse(lpath, None)
            if base is None:
                results.append("  # Break, base is none")
                continue
            basepath = "/".join(base.getPhysicalPath())
            if lpath != basepath:
                results.append("  # Break, requested path not basepath (%s != %s)" % (lpath,basepath))
                continue
            kw['lang'] = lang
            res = method(base, *args, **kw)
            results.append("Exec: %s for %s" % (method.__name__, lang))
            if res:
                results += list(res)
                
        return results
    
    
    def blockPortlets(self, manager, status):
        """ Block the Portlets on a given context, manager, and Category """
        def _setter(ob, *args, **kw):
            manager = kw['manager']
            status = kw['status']
            CAT = CONTEXT_CATEGORY
            portletManager = getUtility(IPortletManager, name=manager)
            assignable = getMultiAdapter((ob, portletManager,), ILocalPortletAssignmentManager)
            assignable.setBlacklistStatus(CAT, status)
        return self._forAllLangs(_setter, manager=manager, status=status)
    
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
    
    
    def setExcludeFromNav(self, flag):
        """ Sets the Exclude From nav flag """
        def _setter(ob, *args, **kw):
            flag = kw['flag']
            ob.setExcludeFromNav(flag)
        return self._forAllLangs(_setter, flag=flag)

    def setEnableNextPrevious(self, flag):
        """ Enables the Next-Previous Navigation Flag """
        def _setter(ob, *args, **kw):
            flag = kw['flag']
            ob.setNextPreviousEnabled(flag)
        return self._forAllLangs(_setter, flag=flag)
        
    def setTitle(self, title):
        """ simply set the title to a given value. Very primitive! """
        def _setter(ob, *args, **kw):
            title = kw['title']
            ob.setTitle(title)
        return self._forAllLangs(_setter, title=title)
    
    def renamer(self, oldid, newid):
        """ rename one object within context from oldid to newid """
        def _setter(ob, *args, **kw):
            oldid = kq['oldid']
            newid = kw['newid']
            if oldid in ob.objectIds():
                ob.manage_renameObjects([oldid], [newid])
        return self._forAllLangs(_setter, oldid=oldid, newid=newid)
        
    def fixOrder(self, ORDER):
        """Move contents of a folter into order
            make sure the ordering of the folders is correct
        """
        plone_utils = getToolByName(self.context, 'plone_utils')
        def _orderIDs(base, *args, **kw):
            """sorts the objects in base in the order given by ids"""
            results = []
            ids = [x for x in kw['ids']]
            base_ids = base.objectIds()
            results.append('  > current order: %s' % str(base_ids))            
            flag = 0
            if len(base_ids)>= len(ids) and base_ids[:len(ids)] == ids:
                return

            ids.reverse() # we let the items bubble up, last one first

            for id in ids:
                if id in base_ids:
                    flag = 1
                    base.moveObjectsToTop(id)
            if flag == 1: # only reindex if there is something to do
                plone_utils.reindexOnReorder(base)
            results.append("  > New order: %s " % str(base.objectIds()))
            return results
                            
        return self._forAllLangs(_orderIDs, ids=ORDER)          
                
    def deleter(self, id):
        """ deletes an object with a given id from all language branches """
        def _setter(ob, *args, **kw):
            id = kw['id']
            if id in ob.objectIds():
                ob._delObject(id)
        return self._forAllLangs(_setter, id=id)
        
    def propagatePortlets(self):
        """ propagates the portlet config from context to the language versions """
        context = Acquisition.aq_inner(self.context)
        path = "/".join(context.getPhysicalPath()) 
        left = assignment_mapping_from_key(context, 'plone.leftcolumn', CONTEXT_CATEGORY, path)
        right = assignment_mapping_from_key(context, 'plone.rightcolumn', CONTEXT_CATEGORY, path)
        belowcontext = assignment_mapping_from_key(context, 'osha.belowcontent.portlets', CONTEXT_CATEGORY, path)
        
        def _setter(ob, *args, **kw):
            results = []
            cleft = kw['cleft']
            cright = kw['cright']
            cbelowcontext = kw['cbelowcontext']
            
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

        return self._forAllLangs(_setter, cleft=left, cright=right, cbelowcontext=belowcontext)
        
    def setProperty(self, id, typ, value):
        """ sets a OFS Property on context """
        def _setter(ob, *args, **kw):
            id = kw['id']
            typ = kw['typ']
            value = kw['value']
            
            ob = Acquisition.aq_inner(ob)
            if Acquisition.aq_base(ob).hasProperty(id):
                ob._delProperty(id)
            ob._setProperty(id=id, value=value, type=typ)

        return self._forAllLangs(_setter, id=id, typ=typ, value=value)

    def delProperty(self, id):
        """ removes a OFS Property on context """
        def _setter(ob, *args, **kw):
            id = kw['id']
            ob = Acquisition.aq_inner(ob)
            if Acquisition.aq_base(ob).hasProperty(id):
                ob._delProperty(id)
            
        return self._forAllLangs(_setter, id=id)
        
    def setTranslatedTitle(self, label, domain):
        """ sets the title based on the translation availble for title in the language """
        def _setter(ob, *args, **kw):
            translate = getTranslationService().translate
            label = kw['label']
            domain=kw['domain']
            lang = kw['lang']
            title_trans = translate(target_language=lang, msgid=label, default=label, context=ob, domain=domain)
            ob.setTitle(title_trans)
        return self._forAllLangs(_setter, label=label, domain=domain)
            
    def setTranslatedDescription(self, label, domain):
        """ sets the description based on the translation availble for title in the language """
        def _setter(ob, *args, **kw):
            translate = getTranslationService().translate
            label = kw['label']
            domain=kw['domain']
            lang = kw['lang']
            desc_trans = translate(target_language=lang, msgid=label, default=label, context=ob, domain=domain)
            ob.setDescription(desc_trans)
        return self._forAllLangs(_setter, label=label, domain=domain)
            
    def createFolder(self, id, excludeFromNav=True):
        """ creates a folder and all translations in the language branches """
        self.context.invokeFactory('Folder', id)
        ob = getattr(self.context, id)
        ob.unmarkCreationFlag()
        ob.setExcludeFromNav(excludeFromNav)
        for lang in self.langs:
            if lang == self.context.Language():
                continue
            ob.addTranslation(lang)
        return ['Folder Created']


    def cutAndPaste(self, sourcepath, id, targetpath):
        """ uses OFS to cur and paste an object
            sourecpath must refer to the folder which contains the object to move
            id must be a string containing the id of the object to move
            targetpath must be the folder to move to
            both paths must contain one single %s to place the language
        """
        context = Acquisition.aq_inner(self.context)
        if '%s' not in sourcepath:
            return ["Wrong sourcepath"]
        if '%s' not in targetpath:
            return ["Wrong targetpath"]

        results = []

        for lang in self.langs:
            results.append("Trying language: %s" % lang)
            
            spath = sourcepath%lang
            source = context.restrictedTraverse(spath, None)
            if source is None:
                results.append("  # Break, source is none")
                continue
            spathtest = "/".join(source.getPhysicalPath())
            if spath != spathtest:
                results.append("  # Break, requested path not sourcepath (%s != %s)" % (spath,spathtest))
                continue

            tpath = targetpath%lang
            target = context.restrictedTraverse(tpath, None)
            if target is None:
                results.append("  # Break, target is none")
                continue
            tpathtest = "/".join(target.getPhysicalPath())
            if tpath != tpathtest:
                results.append("  # Break, requested path not targetpath (%s != %s)" % (tpath,tpathtest))
                continue

            ob = getattr(source, id)
            ob = Acquisition.aq_base(ob)
            if ob is None:
                results.append("  # Break, ob is None!!" )   
            source._delObject(id, suppress_events=True)
            target._setObject(id, ob, set_owner=0, suppress_events=True)
            ob = target._getOb(id)

            notify(ObjectMovedEvent(ob, source, id, target, id))
            notifyContainerModified(source)
            if Acquisition.aq_base(source) is not Acquisition.aq_base(target):
                notifyContainerModified(target)
            ob._postCopy(target, op=1)
            
            results.append("Copy&Paste successful for language %s" %lang)
            
        return results
        
        
    def addLanguageTool(self):
        """ adds a language Tool """
        def _setter(ob, *args, **kw):
            if ob.isPrincipiaFolderish:
                tool = getattr(Acquisition.aq_parent(ob), 'portal_languages')
                if tool.id in ob.objectIds():
                    ob._delObject(tool.id)
                
                newob = tool._getCopy(tool)
                newob._setId(tool.id)
                notify(ObjectCopiedEvent(newob, tool))

                ob._setObject(tool.id, newob)
                newob = ob._getOb(tool.id)
                newob.wl_clearLocks()
                newob._postCopy(ob, op=0)
                newob.manage_afterClone(newob)

                notify(ObjectClonedEvent(newob))
                return ["Added language tool to %s" % ob.getId()]
        return self._forAllLangs(_setter)


    def subtyper(self, subtype):
        """ sets ob to given subtype """
        def _setter(ob, *args, **kw):
            subtype = kw['subtype']
            subtyperUtil = getUtility(ISubtyper)
            if subtyperUtil.existing_type(ob) is None:
                subtyperUtil.change_type(ob, subtype)
                ob.reindexObject()

        return self._forAllLangs(_setter, subtype=subtype)
        
        
    def reindexByPath(self):
        """ reindexes the current context """
        pass        
        
    def reindexer(self):
        """ reindexes an object in all language branches """
        def _setter(ob, *args, **kw):
            ob.reindexObject()
        return self._forAllLangs(_setter)        
        
        
    def publisher(self):
        """ tries to publish all object languages """
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        def _setter(ob, *args, **kw):
            res = []
            try:
                portal_workflow.doActionFor(ob, 'publish')
                res.append("OK Published %s" % "/".join(ob.getPhysicalPath()))
            except Exception, e:
                res.append("ERR publishing %s: %s" % ("/".join(ob.getPhysicalPath()), str(e) ))
            return res
        return self._forAllLangs(_setter)        
        
        
    def translateThis(self, attrs=[]):
        """ Translates the current object into all languages and transferres the given attributes """
        context = Acquisition.aq_inner(self.context)
        if 'title' not in attrs:
            attrs.append('title')
        # Only do this from the canonical
        context = context.getCanonical()
        res = []
        for lang in self.langs:
            if context.hasTranslation(lang):
                res.append("Translation for %s exists" %lang)
                continue
            context.addTranslation(lang)
            trans = context.getTranslation(lang)
            res.append("Added Translation for %s" %lang)
            for attr in attrs:
                val = context.getField(attr).getAccessor(context)()
                trans.getField(attr).getMutator(trans)(val)
                res.append("  > Transferred Attribute %s" % attr)
            if context.portal_type=='Topic':
                # copy the contents as well
                ids = context.objectIds()
                ids.remove('syndication_information')
                
                for id in ids:
                    orig_ob = getattr(context, id)
                    ob = orig_ob._getCopy(context)
                    ob._setId(id)
                    notify(ObjectCopiedEvent(ob, orig_ob))

                    trans._setObject(id, ob)
                    ob = trans._getOb(id)
                    ob.wl_clearLocks()
                    ob._postCopy(trans, op=0)
                    ob.manage_afterClone(ob)

                    notify(ObjectClonedEvent(ob))
    
        
                res.append("  > Transferred Topic contents" )
                        
        return res
        
        
    def setRichDocAttachments(self, flag=False):
        """ Sets the attachment flag on a rich document """
        def _setter(ob, *args, **kw):
            ob.setDisplayAttachments(flag)
        return self._forAllLangs(_setter)        
        
        
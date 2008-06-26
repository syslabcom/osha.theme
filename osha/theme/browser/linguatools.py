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

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class LinguaToolsView(BrowserView):
    implements(ILinguaToolsView)
    template = ViewPageTemplateFile('templates/linguatools.pt')

    def __call__(self):
        self.request.set('disable_border', True)
#        context = Acquisition.aq_inner(self.context)
        
#        portal_catalog = getToolByName(context, 'portal_catalog')
#        portal_languages = getToolByName(context, 'portal_languages')
#        self.lang = portal_languages.getPreferredLanguage()
        if self.request.has_key("form.button.UpdateTitle"):
            title = self.request.get('title', "no Title")
            self.result=self.setTitle(title) 
            
        if self.request.has_key("form.button.propagatePortlets"):
            self.result=self.propagatePortlets() 

        if self.request.has_key("form.button.addLanguageTool"):
            self.result=self.addLanguageTool() 

        if self.request.has_key("form.button.reindexer"):
            self.result=self.reindexer() 

        if self.request.has_key("form.button.publisher"):
            self.result=self.publisher() 

        if self.request.has_key("form.button.hider"):
            self.result=self.hider() 

        if self.request.has_key("form.button.setEnableNextPrevious"):
            self.result=self.setEnableNextPrevious(True) 

        if self.request.has_key("form.button.setDisableNextPrevious"):
            self.result=self.setEnableNextPrevious(False) 

        if self.request.has_key("form.button.setExcludeFromNav"):
            self.result=self.setExcludeFromNav(True) 

        if self.request.has_key("form.button.setIncludeInNav"):
            self.result=self.setExcludeFromNav(False) 

        if self.request.has_key("form.button.setRichDocAttachment"):
            self.result=self.setRichDocAttachment(True) 

        if self.request.has_key("form.button.unsetRichDochAttachment"):
            self.result=self.setRichDocAttachment(False) 

        if self.request.has_key("form.button.deleter"):
            guessLanguage = self.request.get('guessLanguage', '')
            id = self.request.get('id', '')
            self.result=self.deleter(id,guessLanguage) 

        if self.request.has_key("form.button.ChangeId"):
            oldId = self.request.get('oldid', "")
            id = self.request.get('id', oldId)
            self.result=self.renamer(oldId,id) 

        if self.request.has_key("form.button.setTranslateTitle"):
            label = self.request.get('label', "")
            domain = self.request.get('domain', "plone")
            self.result=self.setTranslatedTitle(label,domain) 
            self.result=self.setTranslatedDescription(label,domain) 

        if self.request.has_key("form.button.createFolder"):
            excludeFromNav = self.request.get('excludeFromNav', 'true')
            id = self.request.get('id', '')
            self.result=self.createFolder(id,excludeFromNav) 

        if self.request.has_key("form.button.fixTranslationReference"):
            recursive = self.request.get('recursive', 'false')
            self.result=self.fixTranslationReference(recursive) 

        if self.request.has_key("form.button.subtyper"):
            subtype = self.request.get('subtype', "")
            self.result=self.subtyper(subtype) 

        if self.request.has_key("form.button.delProperty"):
            id = self.request.get('id', "")
            self.result=self.delProperty(id) 

        if self.request.has_key("form.button.blockPortlet"):
            manager = self.request.get('manager', "")
            cat = self.request.get('cat', "")
            status = self.request.get('status', "")
            self.result=self.blockPortlets(manager,cat,status) 
            
        if self.request.has_key("form.button.setProperty"):
            id = self.request.get('id', "")
            typ = self.request.get('typ', "")
            value = self.request.get('value', "")
            self.result=self.setProperty(id,typ,value) 

        if self.request.has_key("form.button.cutAndPaste"):
            sourcepath = self.request.get('sourcepath', "")
            id = self.request.get('id', "")
            value = self.request.get('targetpath', "")
            self.result=self.cutAndPaste(sourcepath,id,targetpath) 
 
        if self.request.has_key("form.button.fixOrder"):
            order = self.request.get('order', "")
            orderlist = order.splitlines(order.count('\n'))
            self.result=self.fixOrder(orderlist) 
        return self.template()

        if self.request.has_key("form.button.translateThis"):
            attrs = self.request.get('attrs', "")
            attrslist = attrs.splitlines(attrs.count('\n'))
            self.result=self.fixOrder(attrslist) 
        return self.template()

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.result = []
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

            base = context.getTranslation(lang)
            if base is None:
                base = context.restrictedTraverse(lpath, None)
                if base is None:
                    results.append("  # Break, base is none")
                    continue
                else:
                    results.append("  # WARNING: obhect found at %s which is not linked as a translation of %s"
                            % (lpath, '/'.join(context.getPhysicalPath()) )) 
#            basepath = "/".join(base.getPhysicalPath())
#            if lpath != basepath:
#                results.append("  # Break, requested path not basepath (%s != %s)" % (lpath,basepath))
#                continue
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
            oldid = kw['oldid']
#             import pdb;pdb.set_trace()
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
                
    def deleter(self, id, guessLanguage=False):
        """ deletes an object with a given id from all language branches """
        def _setter(ob, *args, **kw):
            res = []
            currlang = kw.get('lang', '')
            id = kw['id']
            if id in ob.objectIds():
                ob._delObject(id)
                res.append("deleted %s" %id)
            if guessLanguage==True:
                # Try to also delete objects with id "id_lang.ext"
                stem, ext = id.rsplit('.', 1)
                langname = "%s_%s.%s" %(stem, currlang, ext)
                if langname in ob.objectIds():
                    ob._delObject(langname)
                    res.append("deleted %s" %langname)
            return res
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
        
        
    def addLanguageTool(self, languages=[]):
        """ adds a language Tool """
        def _setter(ob, *args, **kw):
            if ob.isPrincipiaFolderish:
                tool = getattr(Acquisition.aq_parent(ob), 'portal_languages')
                if tool.id in ob.objectIds():
                    ob._delObject(tool.id)
                
                newob = tool._getCopy(tool)
                newob._setId(tool.id)
                notify(ObjectCopiedEvent(newob, tool))

                ob._setOb(tool.id, newob)
                ob._objects = ob._objects+(dict(meta_type=tool.meta_type, id=tool.id),)
                newob = ob._getOb(tool.id)
                newob.wl_clearLocks()
                newob._postCopy(ob, op=0)
                newob.manage_afterClone(newob)

                notify(ObjectClonedEvent(newob))
                if languages:
                    newob.supported_langs = list(languages)
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

    def hider(self):
        """ tries to hide object in all languages """
        portal_workflow = getToolByName(self.context, 'portal_workflow')
        def _setter(ob, *args, **kw):
            res = []
            try:
                portal_workflow.doActionFor(ob, 'hide')
                res.append("OK hidden %s" % "/".join(ob.getPhysicalPath()))
            except Exception, e:
                res.append("ERR hiding %s: %s" % ("/".join(ob.getPhysicalPath()), str(e) ))
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
            flag = kw['flag']
            res = []
            try:
                ob.setDisplayAttachments(flag)
                res.append("OK: set display attachment on %s to %s" % (ob.getId(), flag))
            except Exception, e:
                res.append("ERR setting display attachment on %s (%s)" % ("/".join(ob.getPhysicalPath()), type(Acquisition.aq_base(ob)) ))
            return res
        return self._forAllLangs(_setter, flag=flag)
        
        
    def _guessLanguage(self, filename):
        """
        try to find a language abbreviation in the string
        acceptable is a two letter language abbreviation at the end of the 
        string prefixed by an _ just before the extension
        returns lang, stem, ext
        """
        if callable(filename):
            filename = filename()

        langs = getToolByName(self.context, 'portal_languages').getSupportedLanguages()

        if len(filename)>3 and '.' in filename:
            elems = filename.split('.')
            name = ".".join(elems[:-1])
            if len(name)>3 and name[-3] in ['_', '-']:
                lang = name[-2:].strip()
                lang = lang.lower()
                if lang in langs:
                    namestem = name[:(len(name)-2)]
                    return lang, namestem, elems[-1]

        return '', filename, ''        
        
        
    def _getLangOb(self, ob, lang):
        """ Used by FixTranslationReference
            try to get a matching object in another language path. """
        portal_url = getToolByName(ob, 'portal_url')
        langidx = len(portal_url.getPortalObject().getPhysicalPath())
        obpath = ob.getPhysicalPath()
        langpath = list(obpath)
        langpath[langidx] = lang
        filename = langpath[-1]
        
        specialfilename = ''
        if ob.portal_type in ['File', 'Image']:
            # we try to also accept _xx language abbrevs
            langabbrev, stem, ext = self._guessLanguage(filename)
            if langabbrev !='':
                specialfilename = "%s%s.%s" %(stem, lang, ext)
                
        root = ob.getPhysicalRoot()
        langob = root
        for i in langpath[1:-1]:
            if i in langob.objectIds():
                langob = getattr(langob, i)
            else:
                return None
                
        # now only the filename is left. Special handling:
        if specialfilename !='':               
            langob = getattr(langob, filename, getattr(langob, specialfilename, None))
        else:       
            langob = getattr(langob, filename, None)

        return langob

    def fixTranslationReference(self, recursive=False):
        """ fixes translation references to the canonical.
            Assumes that self is always en and canonical
            tries to handle language extensions for files like hwp_xx.swf
        """
        context = Acquisition.aq_inner(self.context)
        pl = context.portal_languages
        langs = pl.getSupportedLanguages()

        results = []
        if recursive==True:
            targetobs = context.ZopeFind(context, search_sub=1)
        else:
            targetobs = [(context.getId(), context)]
        for id, ob in targetobs:

            print "handling %s" % ob.absolute_url(1)
            if hasattr(Acquisition.aq_base(ob), '_md') and ob._md.has_key('language') and ob._md['language']==u'':
                ob._md['language'] = u'en'

            if not hasattr(Acquisition.aq_base(ob), 'addTranslationReference'):
                continue

            if not ob.isCanonical():
                results.append("Not Canonical: %s " %ob.absolute_url())
                print "Not Canonical: %s " %ob.absolute_url()

            for lang in langs:
                if ob.hasTranslation(lang):           
                    continue
                langob = self._getLangOb(ob, lang)

                if langob is None:
                    continue

                try:
                    langob.setLanguage('')
                    langob.setLanguage(lang)
                    langob.addTranslationReference(ob)
                    langpath = "/".join(langob.getPhysicalPath())
                    results.append( "Adding TransRef for %s" % langpath )
                    print  "Adding TransRef for %s" % langpath
                except Exception, at:
                    results.append( "Except %s" % str(at))

        results.append("ok")
        return results

        

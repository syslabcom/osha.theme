from zope.interface import implements
from Acquisition import aq_base, aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from osha.theme.browser.interfaces import IOSHContentSwitcher, ISwitchOSHContent
from zope.component import getUtility
from Products.OSHContentLink.interfaces import IOSH_Link
from Products.RemoteProvider.content.interfaces import IProvider
from zope.annotation.interfaces import IAnnotations
from Products.statusmessages.interfaces import IStatusMessage
from osha.theme.config import *

COMMON_FIELDS = ['title',  'remoteUrl', 'remoteLanguage', 'country', 'subcategory', 'multilingual_thesaurus', 'nace', ]


class OSHContentSwitcher(BrowserView):
    implements(IOSHContentSwitcher)

    def __call__(self):
        self.uid = self.request.get('uid', '')
        return self.index()

    def getName(self):
        return self.__name__

    def getContentInfo(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        res = portal_catalog(UID=self.uid)
        if len(res) == 0:
            return None
        res_map = [x for x in res]
        # We might actually find more than one result for our UID
        # This happens when we have stale catalog entries
        # Therefore test all results and use the one that is valid
        while len(res_map):
            try:
                xx = res_map.pop()
                obj = xx.getObject()
                break
            except:
                obj = None
        if obj is None:
            return None
        portal_type = obj.portal_type

        existing_url = ''
        ann = IAnnotations(obj)
        existing_uid = ann.get(EXISTING_SWITCHED_CONTENT_UID, '')
        if existing_uid:
            res = portal_catalog(UID=existing_uid)
            existing = len(res) and res[0].getObject()
            existing_url = existing and existing.absolute_url()
        target_type = portal_type == 'OSH_Link' and 'Provider' or 'OSH Resource'
        portal_type = portal_type == 'OSH_Link' and 'OSH Resource' or 'Provider'
        return dict(uid=self.uid,
                portal_type=portal_type,
                target_type=target_type,
                id=obj.getId(),
                existing_url=existing_url,
                title=obj.Title())


class SwitchOSHContent(BrowserView):
    implements(ISwitchOSHContent)

    def __call__(self, skipRedirect=False, **args):
        context = self.context
        request = context.REQUEST
        status = IStatusMessage(request)
        errors = list()
        plone_utils = getToolByName(context, 'plone_utils')
        id = request.get('id')
        uid = request.get('uid')

        if IProvider.providedBy(context):
            target = context.restrictedTraverse('/osha/portal/data/links')
            if not target:
                 errors.append("Error: folder for adding the OSH Resource could not be found")
            else:
                if getattr(aq_base(target), id, None):
                    errors.append("The ID '%s' already exists as an OSH Resource."
                    " Please choose a different id" %id)
                else:
                    target.invokeFactory(id=id, type_name="OSH_Link")
                    obj = getattr(target, id)
                    for fname in COMMON_FIELDS:
                        value = context.getField(fname).getAccessor(context)()
                        obj.getField(fname).getMutator(obj)(value)
                    obj.setText(context.Description())
                    obj.reindexObject()
                    ann = IAnnotations(context)
                    ann[EXISTING_SWITCHED_CONTENT_UID] = obj.UID()
                    status.addStatusMessage("Switching content was successful! See the box below for a link to "
                    "the new OSH Resource.", type='info')
                    try:
                        pwt = getToolByName(context, 'portal_workflow')
                        pwt.doActionFor(context, 'delete')
                        status.addStatusMessage("The workflow state on this Provider was set to 'deleted'",
                            type='info')
                    except:
                         status.addStatusMessage("Setting the workflow state to 'deleted' was NOT possible.",
                            type="warning")
        elif IOSH_Link.providedBy(context):
            target = context.restrictedTraverse('/osha/portal/data/provider')
            if not target:
                 errors.append("Error: folder for adding the Provider could not be found")
            else:
                if getattr(aq_base(target), id, None):
                     errors.append("The ID '%s' already exists as a Provider. Please choose a different id" %id)
                else:
                    target.invokeFactory(id=id, type_name="Provider")
                    obj = getattr(target, id)
                    for fname in COMMON_FIELDS:
                        value = context.getField(fname).getAccessor(context)()
                        obj.getField(fname).getMutator(obj)(value)
                    obj.setDescription(context.getText())
                    obj.reindexObject()
                    ann = IAnnotations(context)
                    ann[EXISTING_SWITCHED_CONTENT_UID] = obj.UID()
                    status.addStatusMessage("Switching content was successful! See the box below for a link to "
                    "the new Provider.", type='info')
                    try:
                        pwt = getToolByName(context, 'portal_workflow')
                        pwt.doActionFor(context, 'delete')
                        status.addStatusMessage("The workflow state on this OSH Resource was set to 'deleted'",
                            type='info')
                    except:
                         status.addStatusMessage("Setting the workflow state to 'deleted' was NOT possible.",
                            type="warning")
        else:
            errors.append('This form was used on content other than a Provider or OSH Resource.')

        if len(errors):
            path = "%s/oshcontent_switch_form?uid=%s&id=%s" % (context.absolute_url(), uid, id)
            for error in errors:
                status.addStatusMessage(error, type="error")
        else:
            path = context.absolute_url()
        self.request.RESPONSE.redirect(path)

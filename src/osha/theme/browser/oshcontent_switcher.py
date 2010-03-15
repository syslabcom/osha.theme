from zope.interface import implements
from Acquisition import aq_base, aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from osha.theme.browser.interfaces import IOSHContentSwitcher, ISwitchOSHContent
from zope.component import getUtility
from Products.OSHContentLink.interfaces import IOSH_Link
from Products.RemoteProvider.content.interfaces import IProvider
from zope.annotation.interfaces import IAnnotations
from osha.theme.config import *

LinkToProvider = ['title',  'remoteUrl', 'remoteLanguage', 'country', 'subcategory', 'multilingual_thesaurus', 'nace', ]


class OSHContentSwitcher(BrowserView):
    implements(IOSHContentSwitcher)

    template = ViewPageTemplateFile('templates/oshcontent_switch_form.pt')
    template.id = "oshcontent_switch_form"

    def __call__(self):
        self.uid = self.request.get('uid', '')
        return self.template()

    def getContentInfo(self):
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        res = portal_catalog(UID=self.uid)
        if len(res) == 0:
            return None
        obj = res[0].getObject()
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
        target_type = portal_type == 'OSH_Link' and 'Provider' or 'OSH_Link'
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
        plone_utils = getToolByName(context, 'plone_utils')
        id =request.get('id')


        if IProvider.providedBy(context):
            message = "provider!"
        elif IOSH_Link.providedBy(context):
            target = context.restrictedTraverse('/osha/portal/data/provider')
            if not target:
                message = "Error: folder for adding the Provider could not be found"
            else:
                if getattr(aq_base(target), id, None):
                    message = "The ID '%s' already exists as a Provider. Please choose a different id"
                else:

                    #import pdb; pdb.set_trace()
                    target.invokeFactory(id=id, type_name="Provider")
                    obj = getattr(target, id)
                    for fname in LinkToProvider:
                        value = context.getField(fname).getAccessor(context)()
                        obj.getField(fname).getMutator(obj)(value)
                    obj.setDescription(context.getText())
                    obj.reindexObject()
                    ann = IAnnotations(context)
                    ann[EXISTING_SWITCHED_CONTENT_UID] = obj.UID()
                    message = "Switching content was successful!"
                    try:
                        pwt = getToolByName(context, 'portal_workflow')
                        pwt.doActionFor(context, 'delete')
                        message += "\nSet workflow state to 'deleted'"
                    except:
                        message += "Setting workflow state to 'deleted' was NOT possible"


        else:
            message = "An error occurred"


        if not skipRedirect:
            path = context.absolute_url()
            plone_utils.addPortalMessage(message)
            self.request.RESPONSE.redirect(path)
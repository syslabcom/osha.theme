from zope.interface import implements
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from osha.theme.browser.interfaces import IOSHContentSwitcher
from zope.component import getUtility


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
        target_type = portal_type == 'OSH_Link' and 'Provider' or 'OSH_Link'
        return dict(uid=self.uid,
                portal_type=portal_type,
                target_type=target_type,
                title=obj.Title())

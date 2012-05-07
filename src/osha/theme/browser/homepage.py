from zope.i18nmessageid import MessageFactory
from zope.interface import implements

import Acquisition
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.memoize import ram
from DateTime import DateTime
from Products.ATContentTypes.interface.document import IATDocument
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

_ = MessageFactory('osha.theme')


class HomepageView(BrowserView):

    # Remove this for Plone 4
    template = ViewPageTemplateFile('templates/osha_homepage.pt')
    template.id = "osha_homepage"
    # and move it to the template= statement in configure.zcml

    def __init__(self, context, request=None):
        self.context = context
        self.ptool = getToolByName(context, 'portal_url')
        self.ltool = getToolByName(context, 'portal_languages')
        self.pref_lang = self.ltool.getPreferredLanguage()
        self.portal = self.ptool.getPortalObject()
        self.portal_path = '/'.join(self.portal.getPhysicalPath())
        self.langroot = getattr(self.portal, self.pref_lang, \
            getattr(self.portal, 'en'))

    def __call__(self):
        return self.template()

    # For Plone 4
    # def __call__(self):
    #     return self.index()

    @property
    def intro(self):
        intro = getattr(self.langroot, 'intro-page', None)
        if intro is None:
            return dict(title='No introduction found', link='#')
        else:
            return dict(title=intro.Title(), link=intro.absolute_url())

    @property
    def highlights(self, limit=4):
        """Fetch the latest X teasers"""
        portal_path = self.ptool.getPortalPath()
        pc = getToolByName(self.context, 'portal_catalog')
        portal_transforms = getToolByName(self.context, 'portal_transforms')
        ploneview = self.context.restrictedTraverse('@@plone')
        end = {'query': DateTime(), 'range': 'min'}
        res = pc(portal_type='News Item',
            Language=[self.pref_lang, ''],
            sort_order='reverse', sort_on='effective',
            expires={'query': DateTime(), 'range': 'min'},
            path=['%s/%s/teaser' % (self.portal_path, self.pref_lang)])
        if len(res) and limit > 0:
            res = res[:limit]
        if len(res) == 0:
            now = DateTime()
            return [dict(link='', description='No highlights were found',
                        title='No Highlights', img_url='', date=DateTime())]
        ret = list()
        for r in res:
            obj = r.getObject()
            link = obj.absolute_url()
            img_url = obj.getImage() and \
                '/'.join(obj.getImage().getPhysicalPath()) or ''
            # use 'mini' scale
            img_url = img_url.replace('/image', '/image_mini')
            description = obj.Description().strip() != '' and \
                obj.Description() or obj.getText()
            if not isinstance(description, unicode):
                description = description.decode('utf-8')
            description = portal_transforms.convert('html_to_text', description).getData()
            description = ploneview.cropText(description, length=400,
            ellipsis="...")
            date = obj.effective()
            ret.append(dict(link=link, img_url=img_url, description=description,
                title=obj.Title(), date=date))
        return ret

    @property
    def in_focus(self, limit=4):
        """Fetch the latest X In Focus news"""
        portal_path = self.ptool.getPortalPath()
        pc = getToolByName(self.context, 'portal_catalog')
        end = {'query': DateTime(), 'range': 'min'}
        res = pc(portal_type='News Item',
            Language=[self.pref_lang, ''],
            sort_order='reverse', sort_on='effective',
            expires={'query': DateTime(), 'range': 'min'},
            path=['%s/%s/in-focus' % (self.portal_path, self.pref_lang)])
        if len(res) and limit > 0:
            res = res[:limit]
        if len(res) == 0:
            now = DateTime()
            yield dict(link='', description='No items for In Focus were found',
                        title='No Focus', img_url='', date=DateTime())
        for r in res:
            obj = r.getObject()
            link = obj.absolute_url()
            img_url = obj.getImage() and \
                '/'.join(obj.getImage().getPhysicalPath()) or ''
            # use 'thumb' scale
            img_url = img_url.replace('/image', '/image_thumb')
            description = obj.Description().strip() != '' and \
                obj.Description() or obj.getText()
            if not isinstance(description, unicode):
                description = description.decode('utf-8')
            date = obj.effective()
            yield dict(link=link, img_url=img_url, description=description,
                title=obj.Title(), date=date)

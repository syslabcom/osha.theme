from BeautifulSoup import BeautifulSoup
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('osha.theme')

ALLOWED_TAGS = [
    "p", "br", "ul", "ol", "li", "sub", "sup", "abbr", "acronym",
    "dl", "dt", "dd", "cite",
]


def stripHTML(text):
    soup = BeautifulSoup(text)
    for tag in soup.findAll(True):
        if tag.name not in ALLOWED_TAGS:
            tag.extract()
    return soup.renderContents()


class HomepageView(BrowserView):

    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        self.ptool = getToolByName(context, 'portal_url')
        self.ltool = getToolByName(context, 'portal_languages')
        self.pref_lang = self.ltool.getPreferredLanguage()
        self.portal = self.ptool.getPortalObject()
        self.portal_path = '/'.join(self.portal.getPhysicalPath())
        self.langroot = getattr(
            self.portal, self.pref_lang, getattr(self.portal, 'en'))

    def __call__(self):
        return self.index()

    @property
    def intro(self):
        intro = getattr(self.langroot, 'about', None)
        if intro is None:
            return dict(title='No introduction found', link='#')
        else:
            return dict(link=intro.absolute_url())

    @property
    def highlights(self, limit=4):
        """Fetch the latest X teasers"""
        pc = getToolByName(self.context, 'portal_catalog')
        portal_transforms = getToolByName(self.context, 'portal_transforms')
        ploneview = self.context.restrictedTraverse('@@plone')
        now = DateTime()
        res = pc(
            portal_type=['News Item'],
            Language=[self.pref_lang, ''],
            sort_order='reverse', sort_on='effective',
            expires={'query': now, 'range': 'min'},
            effective={'query': now, 'range': 'max'},
            review_state='published',
            path=['%s/%s/teaser' % (self.portal_path, self.pref_lang)]
        )
        if len(res) and limit > 0:
            res = res[:limit]
        if len(res) == 0:
            now = DateTime()
            return [
                dict(
                    link='',
                    description='No highlights were found',
                    title='No Highlights',
                    img_url='',
                    date=DateTime(),
                )
            ]
        ret = list()
        for r in res:
            obj = r.getObject()
            link = obj.absolute_url()
            img_url = obj.getImage() and \
                obj.getImage().absolute_url() or ''
            # use 'mini' scale
            img_url = img_url.replace('/image', '/image_mini')
            description = obj.Description().strip() != '' and \
                obj.Description() or obj.getText()
            if not isinstance(description, unicode):
                description = description.decode('utf-8')
            date = obj.effective()
            ret.append(
                dict(
                    link=link,
                    img_url=img_url,
                    description=description,
                    title=obj.Title(),
                    date=date,
                )
            )
        return ret

    @property
    def in_focus(self, limit=6):
        """Fetch the latest X In Focus news"""
        pc = getToolByName(self.context, 'portal_catalog')
        now = DateTime()
        res = pc(
            portal_type=['News Item'],
            Language=[self.pref_lang, ''],
            sort_order='reverse', sort_on='effective',
            expires={'query': now, 'range': 'min'},
            effective={'query': now, 'range': 'max'},
            review_state='published',
            path=['%s/%s/in-focus' % (self.portal_path, self.pref_lang)]
        )
        if len(res) and limit > 0:
            res = res[:limit]
        if len(res) == 0:
            now = DateTime()
            yield dict(
                link='',
                description='No items for In Focus were found',
                title='No Focus',
                img_url='',
                external_link='',
                date=DateTime(),
            )
        for r in res:
            obj = r.getObject()
            link = obj.absolute_url()
            field = obj.getField('external_link')
            external_link = field and field.getRaw(obj) or ''
            img_url = obj.getImage() and \
                obj.getImage().absolute_url() or ''
            # use 'thumb' scale
            img_url = img_url.replace('/image', '/image_thumb')
            description = obj.Description().strip() != '' and \
                obj.Description() or obj.getText()
            if not isinstance(description, unicode):
                description = description.decode('utf-8')
            date = obj.effective()
            yield dict(
                link=link,
                img_url=img_url,
                description=description,
                title=obj.Title(),
                date=date,
                external_link=external_link,
            )

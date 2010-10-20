from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from osha.theme.browser.interfaces import ICompetitionsView, ICompetitionDetail
from Products.Archetypes.interfaces._base import IBaseContent, IBaseFolder
from Products.ATContentTypes.interface.image import IATImage
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Acquisition import aq_parent, aq_inner


class CompetitionsView(BrowserView):
    implements(ICompetitionsView)

    template = ViewPageTemplateFile('templates/competitions_view.pt')
    template.id = "competitions-view"

    def __call__(self):
        return self.template()

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.now = DateTime()
        if IBaseFolder.providedBy(context):
            self.parent = context
        else:
            self.parent = aq_parent(aq_inner(context))
        self.path = '/'.join(self.parent.getPhysicalPath())

    def getUpcoming(self):
        context = self.context
        upcoming = list()
        catalog = getToolByName(context, 'portal_catalog')
        res = catalog(portal_type='Folder', path=self.path,
            review_state='published',
            effective=dict(query=self.now, range='min'))
        for r in res:
            folder = r.getObject()
            img = ''
            item = folder
            default_view = getattr(folder, folder.defaultView())
            if IBaseContent.providedBy(default_view):
                img = self.getRelatedImage(default_view)
                item = default_view
            upcoming.append(dict(item=item, img=img))
        return upcoming

    def getRelatedImage(self, obj):
        """
        Return html for a video, slideshow or image from the related
        items of the canonical translation.
        """
        obj = obj.getCanonical()
        related_items = obj.getRelatedItems()
        images = [i for i in related_items if IATImage.providedBy(i)]
        if len(images) > 0:
            image = images[0]
            return image.absolute_url()
        return ''


class CompetitionDetail(BrowserView):
    implements(ICompetitionDetail)

    template = ViewPageTemplateFile('templates/competition_detail.pt')
    template.id = "competition-detail"

    def __call__(self):
        return self.template()

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
        """ Get upcoming competitions """
        query = dict(portal_type='Folder', path=self.path,
            review_state='published',
            effective=dict(query=self.now, range='min'))
        return self._getCompetitionsWithImages(query)

    def getOngoing(self):
        """ Get ongoing competitions """
        query = dict(portal_type='Folder', path=self.path,
            review_state='published',
            effective=dict(query=self.now, range='max'),
            expires=dict(query=self.now, range='min'))
        return self._getCompetitionsWithImages(query)

    def _getCompetitions(self, query):
        catalog = getToolByName(self.context, 'portal_catalog')
        competitions = list()
        res = catalog(query)
        for r in res:
            folder = r.getObject()
            competitions.append(folder)
        return competitions

    def _getCompetitionsWithImages(self, query):
        result = list()
        competitions = self._getCompetitions(query)
        for competition in competitions:
            images = ''
            default_view = getattr(competition, competition.defaultView())
            item = competition
            if IBaseContent.providedBy(default_view):
                images = self.getRelatedImages(default_view, 'mini')
                item = default_view
            result.append(dict(item=item, images=images))
        return result

    def getRelatedImages(self, obj, image_scale):
        """
        Return html for a video, slideshow or image from the related
        items of the canonical translation.
        """
        scaled = list()
        obj = obj.getCanonical()
        related_items = obj.getRelatedItems()
        images = [i for i in related_items if IATImage.providedBy(i)]
        # Limit to three
        images = images[:3]
        for image in images:
            scaled_img = image.getField('image').getScale(image,
                scale=image_scale)
            scaled.append(scaled_img.absolute_url())
        return scaled


class CompetitionDetail(CompetitionsView):
    implements(ICompetitionDetail)

    template = ViewPageTemplateFile('templates/competition_detail.pt')
    template.id = "competition-detail"

    def __call__(self):
        return self.template()

    def getTeaserImage(self):
        images = self.getRelatedImages(self.context, 'mini')
        return len(images) and images[0] or ''

    def thisyear(self):
        " return this years number "
        return self.now.year()
        
    def lastyear(self):
        " return last years number "
        return self.now.year()-1

    def getClosed(self):
        " get closed competitions "
        query = dict(portal_type='Folder', path=self.path,
            review_state='published',
            effective=dict(query=self.now, range='max'),
            expires=dict(query=self.now, range='max'))

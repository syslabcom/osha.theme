from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from osha.theme.browser.interfaces import ICompetitionsView, ICompetitionDetail
from Products.Archetypes.interfaces._base import IBaseContent, IBaseFolder
from Products.ATContentTypes.interface.image import IATImage
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime
from Acquisition import aq_parent, aq_inner, aq_base
from plone.memoize.instance import memoize


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
            review_state='published', show_inactive=True,
            effective=dict(query=self.now, range='min'))
        competitions = self._getCompetitionsWithImages(query)
        print "upcoming:", competitions
        return competitions

    def getOngoing(self):
        """ Get ongoing competitions """
        query = dict(portal_type='Folder', path=self.path,
            review_state='published', show_inactive=True,
            effective=dict(query=self.now, range='max'),
            expires=dict(query=self.now, range='min'))
        competitions = self._getCompetitionsWithImages(query)
        print "ongoing:", competitions
        return competitions

    # @memoize
    def getClosed(self):
        " get closed competitions "
        query = dict(portal_type='Folder', path=self.path,
            review_state='published', show_inactive=True,
            effective=dict(query=self.now, range='max'),
            expires=dict(query=self.now, range='max'))
        competitions = self._getCompetitions(query)
        return self.sortByDate(competitions)

    # @memoize
    def sortByDate(self, competitions):
        yearmap = dict()
        for competition in competitions:
            date = competition.effective()
            yearlist = yearmap.get(date.year(), [])
            yearlist.append((date.month(), dict(id=competition.getId(),
                                        url=competition.absolute_url(),
                                        title=competition.Title()),
                                ))
            yearmap[date.year()] = yearlist

        for year in yearmap.keys():
            yearlist = yearmap[year]
            yearlist.sort()
            yearlist.reverse()
            yearmap[year] = yearlist

        return yearmap

    def getThisyearsCompetitions(self):
        " get closed competitions from this year "
        yearmap = self.getClosed()
        return yearmap.get(self.thisyear(), [])

    def getLastyearsCompetitions(self):
        " get closed competitions from last year "
        yearmap = self.getClosed()
        return yearmap.get(self.lastyear(), [])

    def getOldCompetitions(self):
        " return all other newsletters older than last years "
        yearmap = self.getClosed()
        if self.thisyear() in yearmap.keys():
            del yearmap[self.thisyear()]
        if self.lastyear() in yearmap.keys():
            del yearmap[self.lastyear()]
        return yearmap

    def _getCompetitions(self, query):
        catalog = getToolByName(self.context, 'portal_catalog')
        competitions = list()
        res = catalog(**query)
        context_folder = self.context.restrictedTraverse(self.path)
        for r in res:
            folder = r.getObject()
            if folder != context_folder:
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

    def thisyear(self):
        " return this years number "
        return self.now.year()

    def lastyear(self):
        " return last years number "
        return self.now.year() - 1

    def moreAboutEditable(self):
        f = self._getfile()
        mtool = getToolByName(self.context, 'portal_membership')
        return mtool.checkPermission('Modify portal content', f)

    def moreAboutEditlink(self):
        f = self._getfile()
        return f.absolute_url() + '/edit'

    # @memoize
    def _getfile(self):
        folder = self.context.restrictedTraverse(self.path)
        if getattr(aq_base(folder), 'more-about',
            getattr(aq_base(folder.getCanonical()), 'more-about', None)):
            portlet_moreabout = getattr(folder, 'more-about',
                getattr(folder.getCanonical(), 'more-about', None))
            return portlet_moreabout
        return None

    # @memoize
    def moreAboutContent(self):
        return self._getfile() and self._getfile().getText() or None

    # @memoize
    def moreAboutTitle(self):
        return self._getfile() and self._getfile().Title() or None


class CompetitionDetail(CompetitionsView):
    implements(ICompetitionDetail)

    template = ViewPageTemplateFile('templates/competition_detail.pt')
    template.id = "competition-detail"

    def __init__(self, context, request):
        super(CompetitionDetail, self).__init__(context, request)
        if IBaseFolder.providedBy(context):
            self.parent = aq_parent(aq_inner(context))
        else:
            self.parent = aq_parent(aq_parent(aq_inner(context)))
        self.parent = '/'.join(self.parent.getPhysicalPath())

    def __call__(self):
        return self.template()

    def getTeaserImage(self):
        images = self.getRelatedImages(self.context, 'mini')
        return len(images) and images[0] or ''

    def getClosed(self):
        " get closed competitions "
        query = dict(portal_type='Folder', path=self.parent,
            review_state='published', show_inactive=True)
        competitions = self._getCompetitions(query)
        competitions = [x for x in competitions
            if '/'.join(x.getPhysicalPath()) != self.path]
        return self.sortByDate(competitions)

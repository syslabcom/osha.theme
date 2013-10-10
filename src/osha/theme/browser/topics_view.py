from Acquisition import aq_parent, aq_inner

from Products.ATContentTypes.interface.image import IATImage
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class TopicsBrowserView(BrowserView):
    """
    This class is used for @@topic-view which has a special layout
    which shows related Images at the top, and uses slc.linkcollection
    in the footer
    """
    images = []
    slideswitch_template = ViewPageTemplateFile('templates/slideswitch.pt')
    image_scale = "mini"

    def __call__(self):
        return self.index()

    def getName(self):
        return self.__name__

    def hasRelatedMedia(self):
        """
        Check that the canonical translation has some related images
        or videos.
        """
        context = self.context.getCanonical()
        related_items = context.getRelatedItems()
        media = [i for i in related_items if IATImage.providedBy(i)]
        return media and True or False

    def getRelatedMedia(self, image_scale):
        """
        Return html for a slideshow or image from the related items of
        the canonical translation.
        """
        context = self.context.getCanonical()
        related_items = context.getRelatedItems()

        self.image_scale = image_scale
        if related_items:
            self.images = [
                i for i in related_items if IATImage.providedBy(i)]
            if len(self.images) == 1:
                image = self.images[0]
                return image.tag(scale=image_scale)
            else:
                return self.slideswitch_template()


class TopicsView(TopicsBrowserView):
    """ View class for /topics
    """

    def __call__(self):
        """
        List published sub folders
        """
        context = self.context
        self.parent = aq_parent(aq_inner(context))
        folders = self.parent.getFolderContents(
            {'portal_type':'Folder', 'review_state':'published'}
            )
        middle_index = len(folders) - len(folders) / 2
        self.left_folders = folders[:middle_index]
        self.right_folders = folders[middle_index:]
        return self.index()


class TopicView(TopicsBrowserView):
    """ View class for /topics/topic
    """
    pass


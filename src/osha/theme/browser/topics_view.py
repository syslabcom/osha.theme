from Acquisition import aq_parent, aq_inner
from Products.ATContentTypes.interface.image import IATImage
from Products.CMFCore.interfaces._content import IFolderish
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from p4a.plonevideoembed.interfaces import IVideoLinkEnhanced


class TopicsBrowserView(BrowserView):
    """ A base class for the topic browser views to inherit from """
    images = []
    slideswitch_template = ViewPageTemplateFile('templates/slideswitch.pt')
    image_scale = "mini"

    def hasRelatedMedia(self):
        """ Has some related images or videos.
        """
        context = self.context
        related_items = context.getRelatedItems()
        media = [i for i in related_items if
                 IVideoLinkEnhanced.providedBy(i)
                 or IATImage.providedBy(i)]
        return media and True or False

    def getRelatedMedia(self, video_width, image_scale):
        """ Return a video, slideshow or image.
        """
        context = self.context
        related_items = context.getRelatedItems()
        videos = [i for i in related_items if
                  IVideoLinkEnhanced.providedBy(i)]
        self.image_scale = image_scale
        video_width = int(video_width)
        if videos:
            video = videos[0]
            embed = video.restrictedTraverse("@@video-embed.htm")
            return embed.get_code(width=video_width)
        elif related_items:
            self.images = [i for i in related_items if
                           IATImage.providedBy(i)]
            if len(self.images) == 1:
                image = self.images[0]
                return image.tag(scale=image_scale)
            else:
                return self.slideswitch_template()


class TopicsView(TopicsBrowserView):
    """ View class for /topics
    """
    template = ViewPageTemplateFile('templates/topics_view.pt')
    template.id = "topics-view"

    def __call__(self):
        return self.template()

    def getPracticalSolutions(self):
        """ Practical Solutions are in subfolders at the same level as
        this Rich Document.
        """
        context = self.context
        if IFolderish.providedBy(context):
            context = aq_parent(aq_inner(context))
        practicalSolutions = context.contentValues(
            filter={'portal_type':['Folder']}
            )
        return practicalSolutions


class TopicView(TopicsBrowserView):
    """ View class for /topics/topic
    """
    template = ViewPageTemplateFile('templates/topic_view.pt')
    template.id = "topic-view"

    def __call__(self):
        intro = getattr(self.context, 'introduction_html', None)
        if intro is None:
            self.intro = ''
        else:
            self.intro = intro.CookedBody()
        return self.template()

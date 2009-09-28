from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class TopicsView(BrowserView):
    """ View class for /topics 
    """
    template = ViewPageTemplateFile('templates/topics_view.pt')
    template.id = "topics-view"    

    def __call__(self):
        return self.template() 
        
    def getTopicImages(self):
        """ Get the 10 most recent images from the topic sub sections. """
        context = self.context
        path ="/".join(context.getPhysicalPath())
        pc = getToolByName(context, 'portal_catalog')
        images = pc.searchResults({'portal_type': 'Image',
                                'sort_on': 'effective',
                                'sort_limit': 10,
                                'path': path})
        return images

class TopicView(BrowserView):
    """ View class for /topics/topic 
    """
    template = ViewPageTemplateFile('templates/topic_view.pt')
    template.id = "topic-view"    

    def __call__(self):
        return self.template() 


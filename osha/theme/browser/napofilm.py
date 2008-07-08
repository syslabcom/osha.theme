import Acquisition
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class NapoFilmView(common.ViewletBase):

    _template = ViewPageTemplateFile('templates/napofilmview.pt')
    def __init__(self,context,request):
        self.context=context
        self.request=request
        self.FilmInfo=self.context.napofilmstructure()

    def __call__(self):
        return self._template()

    def listobjects(self):
        context = Acquisition.aq_inner(self.context)
        container = Acquisition.aq_parent(context)
        objects = container.objectValues(['ATDocument', 'RichDocument'])
        ip = container.getDefaultPage()
        filtered_objects = [x for x in objects if x.getId()!=ip]
        return filtered_objects

    def getFilms(self):
        return self.FilmInfo

    def getTitle(self,filmID):
        return self.FilmInfo[filmID]['title']

    def getDescription(self,filmID):
        return self.FilmInfo[filmID]['description']

    def getDURLAVI(self,filmID):
        return self.FilmInfo[filmID]['durl AVI']

    def getDURLWMV(self,filmID):
        return self.FilmInfo[filmID]['durl WMV']


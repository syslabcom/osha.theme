import Acquisition
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import common

class NapoEpisodeView(common.ViewletBase):

    _template = ViewPageTemplateFile('templates/napoepisodesview.pt')

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

    def getFilm(self,filmID):
        return self.FilmInfo[filmID]

    def getEpisodes(self,filmID):
        return self.FilmInfo[filmID]['episodes']

    def getEpisodeTitle(self,filmID,EpisodeNummer):
        return self.FilmInfo[filmID]['episodes'][EpisodenNummer]['title']

    def getEpisodeImage(self,filmID,EpisodeNummer):
        return self.FilmInfo[filmID]['episodes'][EpisodenNummer]['image_url']

    def getEpisodeDURLAVI(self,filmID,EpisodeNummer):
        return self.FilmInfo[filmID]['episodes'][EpisodenNummer]['durlavi']

    def getEpisodeDURLWMV(self,filmID,EpisodeNummer):
        return self.FilmInfo[filmID]['episodes'][EpisodenNummer]['durlwmv']

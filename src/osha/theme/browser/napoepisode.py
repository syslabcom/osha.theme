import Acquisition
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

class NapoEpisodeView(BrowserView):

    _template = ViewPageTemplateFile('templates/napoepisodesview.pt')

    def __init__(self,context,request):
        self.context=context
        self.request=request
        self.FilmInfo=self.context.napofilmstructure()

    def __call__(self):
        return self._template()


    def getFilm(self,filmID):
        for film in self.FilmInfo:
            if film[0]==filmID:
                return film[1]
        return {}                



import Acquisition
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

class NapoFilmView(BrowserView):

    _template = ViewPageTemplateFile('templates/napofilmview.pt')
    def __init__(self,context,request):
        self.context=context
        self.request=request
        self.FilmInfo=self.context.napofilmstructure()

    def __call__(self):
        return self._template()

    def getFilms(self):
        return self.FilmInfo



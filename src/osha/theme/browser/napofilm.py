import Acquisition
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView

from osha.theme.browser.multimedia_view import MultimediaFilmListingView

class NapoFilmView(MultimediaFilmListingView):

    template = ViewPageTemplateFile('templates/napofilmview.pt')
    template.id = "napofilmlisting-view"

import Acquisition
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.browser import BrowserView
from osha.theme.browser.multimedia_view import MultimediaFilmEpisodeListingView


class NapoEpisodeView(MultimediaFilmEpisodeListingView):

    template = ViewPageTemplateFile('templates/napoepisodesview.pt')
    template.id = "napoepisode-view"

from string import Template
from ordereddict import OrderedDict
import os
from urlparse import urljoin
from copy import copy

from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class MultimediaImageFoldersView(BrowserView):
    """
    Photo gallery style folder listing
    """
    template = ViewPageTemplateFile(
        'templates/multimedia_image_folders_view.pt')
    template.id = "multimedia-image-folders-view"

    def __call__(self):
        return self.template()

    def get_image_folders(self):
        """Get an ordered dict of folders and details of their images

        OrderedDict(
            "folder_id1": {
                "title": "Folder 1"
                "images":
                    OrderedDict(
                    "image_1":"Image 1",
                    )
                }
            )
        """
        max_image_folders = 6
        image_folders = OrderedDict()
        for folder in self.context.objectValues():
            if max_image_folders < 1:
                return image_folders
            if folder.portal_type == "Folder":
                images = OrderedDict()
                for image in folder.objectValues():
                    if image.portal_type == "Image":
                        images[image.id] = {"title" : image.title}
                if images:
                    image_folders[folder.id] = {"title" : folder.title,
                                           "images" : images}
                    max_image_folders = max_image_folders - 1
        return image_folders


class MultimediaImageDetailsView(BrowserView):
    template = ViewPageTemplateFile(
        'templates/multimedia_image_details_view.pt')
    template.id = "multimedia-image-details-view"

    def __call__(self):
        return self.template()

    def get_images_in_folder(self):
        """Get an ordered dict of images and titles

        OrderedDict("image_1": "Image 1",)
        """
        images = OrderedDict()
        for image in folder.objectValues():
            if image.portal_type == "Image":
                images[image.id] = image.title
        return images

class FilmsDataMixin(object):
    @property
    def media_url(self):
        return self.context.getProperty(
            "media_url", "http://media.osha.europa.eu/napofilm/")

    def set_movie_defaults(self, movies):
        """Returns an ordered dictionary containing the details for
        the current film and all the episodes belonging to it
        populated with default values unless they have been overridden
        in films_data

        Description, video_width and video_height are only used by the
        main Film (not the episodes)"""
        movie_defaults = OrderedDict()
        for movie in movies:
            movie_id = movie["id"]
            mov = movie_defaults[movie_id] = {}
            mov["title"] = movie.setdefault("title", "heading_"+movie_id)
            mov["description"] = movie.setdefault("description",
                                                  "description_"+movie_id)
            mov["image"] = movie.setdefault(
                "image", urljoin(self.media_url, movie_id+".jpg"))
            mov["video_mp4"] = movie.setdefault(
                "video_mp4", urljoin(self.media_url, movie_id+".mp4"))
            mov["video_ogv"] = movie.setdefault(
                "video_ogv", urljoin(self.media_url, movie_id+".ogv"))
            mov["video_webm"] = movie.setdefault(
                "video_webm",  urljoin(self.media_url, movie_id+".webm"))
            mov["video_width"] = movie.setdefault("video_width", 640)
            mov["video_height"] = movie.setdefault("video_height", 352)
        return movie_defaults

    @property
    def films_data(self):
        """This data structure can be overridden by a Script (Python)
        in the current directory called "films_data"
        """
        if hasattr(self.context, "films_data"):
            # a Script (Python) in the current folder
            return self.context.films_data()
        return [
            { "id"          : "napo-015-safe-moves",
              "title"       : "heading_introduction",
              "description" : "description_introduction",
              "image"       : "Custom image.jpg",
              "video_mp4"   : "Safe moves.mp4",
              "video_ogg"   : "Safe moves.ogg",
              "video_webm"  : "Safe moves.webm",
              "episodes"    : [
                    { "id"         :
                          "napo-015-safe-moves-episode-002-danger-unloading",
                      "title"      : "hai",
                      "image"      : "Heavy Lifting2.jpg",
                      "video_mp4"  : "Heavy Lifting2.mp4",
                      "video_ogg"  : "Heavy Lifing2.ogg",
                      "video_webm" : "Heavy Liftin2g.webm",
                      },
                    { "id"         :
                          "napo-015-safe-moves-episode-001-planning-for-safety",
                      }
                    ]
              }
            ]

class MultimediaFilmListingView(BrowserView, FilmsDataMixin):
    """ List the Films and link to the episode listing view for each
    """
    template = ViewPageTemplateFile(
        'templates/multimedia_film_listing_view.pt')
    template.id = "multimedia-film-listing-view"

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.films = self.set_movie_defaults(self.films_data)

    def __call__(self):
        return self.template()

    def get_video_details(self, film_id):
        for film in self.films_data:
            if film["id"] == film_id:
                film_details = self.set_movie_defaults([film])
                if film.has_key("episodes"):
                    episode_details = self.set_movie_defaults(film["episodes"])
                else:
                    episode_details = {}
                return OrderedDict(
                    film_details.items() + episode_details.items())


class MultimediaFilmEpisodeListingView(BrowserView, FilmsDataMixin):
    """ Display the entire Film and each individual episode belonging
    to that film
    """
    template = ViewPageTemplateFile(
        'templates/multimedia_film_episodes_listing_view.pt')
    template.id = "multimedia-film-episodes-listing-view"

    def __call__(self):
        return self.template()

    def video_fancybox(self):
        """ Using a template to pass in the value for media_url and
        the data structure for the episode details since this doesn't
        seem to be possible in the zpt page template."""
        template_path = os.path.join(
            os.path.dirname(__file__),
            "templates/multimedia_film_episodes_listing_view.js.tpl")
        template_file = open(template_path, "r")
        template = Template(template_file.read())
        videos = dict(self.film_details.items() + self.episodes.items())
        film_vals = self.film_details.values()[0]
        return template.substitute(
            media_url = self.media_url,
            videos = videos,
            video_width = film_vals["video_width"],
            video_height = film_vals["video_height"]
            )

    @property
    def film(self):
        """Get the film data for the selected film"""
        selected_film = self.request.form.get("film", None)
        for film in self.films_data:
            if film["id"] == selected_film:
                return film
        return None

    @property
    def film_details(self):
        return self.set_movie_defaults([self.film])

    @property
    def episodes(self):
        """Set the default values for each episode in the selected
        film.
        """
        return self.set_movie_defaults(self.film["episodes"])

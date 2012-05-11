from string import Template
from ordereddict import OrderedDict
import os
from urlparse import urljoin
from copy import copy

from Acquisition import aq_acquire
from Products.Five.browser import BrowserView
from osha.policy.data.multimedia import napofilm

class LipstickView(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, *args, **kw):
        view = aq_acquire(self.context, self.context.getDefaultLayout())
        self.main_macro = view.macros["content-core"]
        return self.index()


class MultimediaFolderListingView(BrowserView):
    """List folder contents using lipstick.css and for folders display
    the first image in the folder beside the description.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.items = self.get_folder_items()

    def __call__(self):
        return self.index()

    def get_folder_items(self):
        folders = OrderedDict()
        items = OrderedDict()
        for item in self.context.listFolderContents():
            item_id = item.getId()
            item_dict = {"id" : item_id,
                         "title": item.Title(),
                         "description": item.Description(),
                         "item_url": item.absolute_url(),
                         "image_url": "" ,
                         "portal_type": item.portal_type}
            if item_dict["portal_type"] in ["Folder",]:
                folders[item_id] = item_dict
                for folder_item in item.listFolderContents():
                    if folder_item.portal_type == "Image":
                        folders[item_id]["image_url"] = \
                            folder_item.absolute_url()
                        break
            elif item_dict["portal_type"] in ["Image"]:
                item_dict["image_url"] = item.absolute_url()
                items[item_id] = item_dict
            else:
                items[item_id] = item_dict
        return OrderedDict(folders.items() + items.items())


class MultimediaImageFoldersView(BrowserView):
    """
    Photo gallery style folder listing
    """

    def __call__(self):
        return self.index()

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
        image_folders = OrderedDict()
        max_images_per_folder = 10
        for folder in self.context.listFolderContents():
            if folder.portal_type == "Folder":
                images = OrderedDict()
                image_count = 0
                for image in folder.listFolderContents():
                    if image_count >= max_images_per_folder:
                        break
                    if image.portal_type == "Image":
                        images[image.id] = {"title" : image.title}
                        image_count += 1
                if images:
                    image_folders[folder.id] = {"title" : folder.title,
                                                "images" : images}
        return image_folders


class MultimediaImageDetailsView(BrowserView):

    def __call__(self):
        return self.index()

    def get_images_in_folder(self):
        """Get an ordered dict of images and titles

        OrderedDict("image_1": "Image 1",)
        """
        images = OrderedDict()
        for image in folder.listFolderContents():
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
        a list of movies [{"id":"movie1", "title":"Custom title"}]

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
            mov["video_avi"] = movie.setdefault(
                "video_avi",  urljoin(self.media_url, movie_id+".avi"))
            mov["video_wmv"] = movie.setdefault(
                "video_wmv",  urljoin(self.media_url, movie_id+".wmv"))
            mov["video_width"] = movie.setdefault("video_width", 640)
            mov["video_height"] = movie.setdefault("video_height", 352)
        return movie_defaults

    @property
    def films_data(self):
        """This data structure can be overridden by a Script (Python)
        called "multimedia_film_structure"
        """
        if hasattr(self.context, "multimedia_film_structure"):
            # a Script (Python) which can override napofilm.filmstructure
            return self.context.multimedia_film_structure()
        return napofilm.filmstructure


class MultimediaFilmListingView(BrowserView, FilmsDataMixin):
    """ List the Films and link to the episode listing view for each
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.films = self.set_movie_defaults(self.films_data)

    def __call__(self):
        return self.index()

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

    def __call__(self):
        return self.index()

    def video_fancybox(self):
        """ Using a template to pass in the value for media_url and
        the data structure for the episode details since this doesn't
        seem to be possible in the zpt page template."""
        if self.film == None:
            return
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
        selected_film = self.request.form.get("filmid", None)
        for film in self.films_data:
            if film["id"] == selected_film:
                return film
        return None

    @property
    def film_details(self):
        if self.film == None:
            return None
        return self.set_movie_defaults([self.film])

    @property
    def episodes(self):
        """Set the default values for each episode in the selected
        film.
        """
        return self.set_movie_defaults(self.film["episodes"])

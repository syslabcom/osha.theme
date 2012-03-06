import httplib
import unittest
from urlparse import urlparse

from ordereddict import OrderedDict

from osha.theme.browser.multimedia_view import MultimediaFilmEpisodeListingView
from osha.theme.tests.base import OshaThemeTestCase


def resource_exists(url):
    domain_name = urlparse(url)[1]
    conn = httplib.HTTPConnection(domain_name)
    conn.request("HEAD", url)
    return conn.getresponse().status == 200


class TestFilmViewsUnitTests(OshaThemeTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Folder", "multimedia")
        self.film_episode_listing_view = self.portal.unrestrictedTraverse(
            "/plone/multimedia/multimedia-film-episodes-listing-view")
        self.film_episode_listing_view.request.form["filmid"] = \
            "napo-015-safe-moves"

    def test_javascript_substitution(self):
        js = self.film_episode_listing_view.video_fancybox()
        self.assertEquals("$" not in js, True,
                          msg=("A variable in the javascript template has not "
                               "been substituted correctly"))
        self.assertEquals("videos = {" in js, True,
                          msg=("The films data structure has not been "
                               "converted for use by the javascript "
                               "correctly."))

    def test_set_movie_defaults(self):
        movies = [{"id":"movie1"}]
        defaults = self.film_episode_listing_view.set_movie_defaults(movies)
        expected_defaults = OrderedDict(
            [('movie1',
              {'description': 'description_movie1',
               'title': 'heading_movie1',
               'image': 'https://media.osha.europa.eu/napofilm/movie1.jpg',
               'video_height': 352,
               'video_width': 640,
               'video_avi': 'https://media.osha.europa.eu/napofilm/movie1.avi',
               'video_mp4': 'https://media.osha.europa.eu/napofilm/movie1.mp4',
               'video_ogv': 'https://media.osha.europa.eu/napofilm/movie1.ogv',
               'video_webm': 'https://media.osha.europa.eu/napofilm/movie1.webm',
               'video_wmv': 'https://media.osha.europa.eu/napofilm/movie1.wmv',
               })])
        self.assertEquals(defaults, expected_defaults)

    def test_napofilmstructure_remote_files_exist(self):
        missing_resources = []
        view = self.film_episode_listing_view
        films_data = view.set_movie_defaults(view.films_data)

        resource_keys = [
            "image", "video_avi", "video_mp4", "video_ogv",
            "video_webm", "video_wmv" ]

        for film_id in films_data:
            film_details = films_data[film_id]

            for resource_key in resource_keys:
                url = film_details[resource_key]
                if not resource_exists(url):
                    missing_resources.append(url)
            view.request.form["filmid"] = film_id
            for episode_id in view.episodes.keys():
                episode = view.episodes[episode_id]
                for resource_key in resource_keys:
                    url = episode[resource_key]
                    if not resource_exists(url):
                        missing_resources.append(url)
            self.assertEquals(
                missing_resources, [],
                msg="Resources missing: %s" % missing_resources)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFilmViewsUnitTests))
    return suite

import unittest

from ordereddict import OrderedDict

from osha.theme.browser.multimedia_view import MultimediaFilmEpisodeListingView
from osha.theme.tests.base import OshaThemeTestCase


class TestFilmViewsUnitTests(OshaThemeTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory("Folder", "multimedia")
        self.film_episode_listing_view = self.portal.unrestrictedTraverse(
            ("/plone/multimedia"
             "/multimedia-film-episodes-listing-view"))
        self.film_episode_listing_view.request.form["film"] = \
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
               'image': 'http://media.osha.europa.eu/napofilm/movie1.jpg',
               'video_height': 352,
               'video_width': 640,
               'video_ogv': 'http://media.osha.europa.eu/napofilm/movie1.ogv',
               'video_mp4': 'http://media.osha.europa.eu/napofilm/movie1.mp4',
               'video_webm': 'http://media.osha.europa.eu/napofilm/movie1.webm'
               })])
        self.assertEquals(defaults, expected_defaults)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFilmViewsUnitTests))
    return suite

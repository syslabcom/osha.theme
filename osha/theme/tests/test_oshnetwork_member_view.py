from zope.component import getUtility, getMultiAdapter
import unittest
import doctest

from osha.theme.browser import oshnetwork_member_view
from osha.theme.tests.base import OshaThemeTestCase

class TestView(OshaThemeTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def populateSite(self):
        """ Populate the test site with some content. """

        self.portal.invokeFactory("Folder", "en")
        self.portal.en.invokeFactory("Folder", "belgium")
        self.portal.en.belgium.invokeFactory("Document", "index_html")
        ltool = self.portal.portal_languages
        ltool.addSupportedLanguage('nl')

    def test_view_methods(self):
        """ Test the methods in the oshnetwork-member-view class """
        self.populateSite()

        view = self.portal.en.belgium.index_html.restrictedTraverse("@@oshnetwork-member-view")
        localized_path = view.getLocalizedPath("asdf")
        self.assertEquals(localized_path,
                          "/en/asdf")

        # Change the language
        view.context.setLanguage("nl")
        localized_path = view.getLocalizedPath("asdf")
        self.assertEquals(localized_path,
                          "/nl/asdf")

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestView))
    return suite

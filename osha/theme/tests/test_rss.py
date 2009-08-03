from five.localsitemanager import make_objectmanager_site
from osha.policy.adapter.schemaextender import TaggingSchemaExtenderERO
import unittest
from zope.app.component.hooks import setSite as setActiveSite
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.publisher.browser import TestRequest
from osha.policy.tests.base import OSHAPolicyFunctionalTestCase
from osha.theme.tests.base import OshaThemeTestCase
from osha.theme.browser.rssfeeds import RSSFeedsView

class TestRSS(unittest.TestCase):
    def test_feedContainsTitle(self):
        view = RSSFeedsView(None, None)
        view._getTranslatedCategories = lambda: [('1', 'one'), ('2', 'two')]
        view._getPortalPath = lambda: "portal_path"
        view._getPrefferedLanguage = lambda: "en"
        should_be = [{'url': 'portal_path/search_rss?Subject=1&RSSTitle=one&Language=en&review_state=published&sort_on=effective', 'icon': 'topic_icon.gif', 'id': '1', 'title': 'one'}, {'url': 'portal_path/search_rss?Subject=2&RSSTitle=two&Language=en&review_state=published&sort_on=effective', 'icon': 'topic_icon.gif', 'id': '2', 'title': 'two'}]
        and_is = view.subject_feeds()
        self.assertEquals(should_be, and_is)
        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRSS))
    return suite
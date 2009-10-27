from five.localsitemanager import make_objectmanager_site
from Products.Five.testbrowser import Browser
import unittest
from zope.app.component.hooks import setSite as setActiveSite
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.publisher.browser import TestRequest
from osha.policy.tests.base import OSHAPolicyFunctionalTestCase
from osha.theme.tests.base import OshaThemeTestCase, OshaThemeFunctionalTestCase
from osha.theme.browser.rssfeeds import RSSFeedsView
from Testing.ZopeTestCase import utils
from Products.PloneTestCase.setup import portal_owner, default_password

def startZServer(browser=None):
    host, port = utils.startZServer()
    if browser:
        print browser.url.replace('nohost', '%s:%s' % (host, port))

def getBrowser(url):
    browser = Browser()
    browser.open(url)
    browser.getControl(name='__ac_name').value = portal_owner
    browser.getControl(name='__ac_password').value = default_password
    browser.getControl(name='submit').click()
    return browser

class TestRSS(unittest.TestCase):
    def test_feedContainsTitle(self):
        view = RSSFeedsView(None, None)
        view._getTranslatedCategories = lambda: [('1', 'one'), ('2', 'two'), ('3', u'dreiö')]
        view._getPortalPath = lambda: "portal_path"
        view._getPrefferedLanguage = lambda: "en"
        view._getTypesForFeeds = lambda: [{'doc_type' :'doc_type', 
                                           'title' : 'nice title',
                                           'icon' : 'nice icon.png',
                                           'base_url' : '/search_rss?RSSTitle=nice%%20title&%(lang)s/%(sorter)s'}]

        should_be = [{'url': 'portal_path/search_rss?Subject=1&RSSTitle=one&Language=en&review_state=published&sort_on=effective', 
                      'icon': 'topic_icon.gif', 'id': '1', 'title': 'one'}, 
                     {'url': 'portal_path/search_rss?Subject=2&RSSTitle=two&Language=en&review_state=published&sort_on=effective', 
                      'icon': 'topic_icon.gif', 'id': '2', 'title': 'two'},  
                     {'url': 'portal_path/search_rss?Subject=3&RSSTitle=drei%C3%83%C2%B6&Language=en&review_state=published&sort_on=effective', 
                      'icon': 'topic_icon.gif', 'id': '3', 'title': u'drei\xc3\xb6'}]
        and_is = view.subject_feeds()
        self.assertEquals(should_be, and_is)
        
        should_be = [{'url': 'portal_path/search_rss?RSSTitle=nice%20title&en/effective', 
                      'icon': 'nice icon.png', 'id': 'doc_type', 'title': 'nice title'}]
        and_is = view.type_feeds()
        self.assertEquals(should_be, and_is)

class TestOshaRSS(OshaThemeFunctionalTestCase):
    def setUp(self):
        super(TestOshaRSS, self).setUp()
        self.browser = getBrowser(self.portal.absolute_url())
    
    def test_configuration(self):
        url = self.portal.absolute_url() + '/@@rss-feeds'
        self.browser.open(url)
        self.assertTrue('News Items' in self.browser.contents)        
        self.assertTrue('Events' in self.browser.contents)        
        self.assertTrue('Publications' in self.browser.contents)
        self.assertEquals(3, self.browser.contents.count('Latest'))        

        
def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestOshaRSS))
    suite.addTest(unittest.makeSuite(TestRSS))
    return suite
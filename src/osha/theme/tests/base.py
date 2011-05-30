import Products.LinguaPlone
import os
from Globals import package_home
from StringIO import StringIO
from Testing import ZopeTestCase as ztc
from Testing.ZopeTestCase import utils

from plone.browserlayer import utils as browserlayerutils

# # importing LinguaPlone to avoid a problem with circular imports
# # See http://do3cc.blogspot.com/2010/08/dont-catch-import-errors-use.html
# # The problem begins here:
# # Products/PloneTestCase/setup.py:
# # ZopeTestCase.installProduct('CMFPlone', quiet=1)

from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.Five.testbrowser import Browser
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase import layer
from Products.PloneTestCase.setup import portal_owner, default_password

from osha.policy.interfaces import IOSHACommentsLayer
from osha.theme.config import product_globals

def startZServer(browser=None):
    """Use this to start the temporary instance being used for
    testing, very useful for debugging tests"""
    host, port = utils.startZServer()
    if browser:
        print browser.url.replace('nohost', '%s:%s' % (host, port))


SiteLayer = layer.PloneSite

class OshaThemeLayer(SiteLayer):

    @classmethod
    def setUp(cls):
        """ The osha.theme package depends on osha.policy so the packages imported
            by the osha.policy tests base.py are also imported and configured here.
        """
        PRODUCTS = [
                'osha.policy',
                ]
        ptc.setupPloneSite(products=PRODUCTS)

        ztc.installProduct('ATCountryWidget')
        ztc.installProduct('ATVocabularyManager')
        ztc.installProduct('LinguaPlone')
        ztc.installProduct('PressRoom')
        ztc.installProduct('PlacelessTranslationService')
        ztc.installProduct('PloneLanguageTool')
        ztc.installProduct('ProxyIndex')
        ztc.installProduct('Relations')
        ztc.installProduct('RichDocument')
        ztc.installProduct('SimpleAttachment')
        ztc.installProduct('TextIndexNG3')
        ztc.installProduct('GroupUserFolder')

        ztc.installPackage('Products.PlacelessTranslationService')
        ztc.installPackage('osha.legislation')
        ztc.installPackage('osha.policy')
        ztc.installPackage('osha.theme')
        ztc.installPackage('slc.seminarportal')
        ztc.installPackage('slc.shoppinglist')

        fiveconfigure.debug_mode = True
        import p4a.subtyper
        zcml.load_config('configure.zcml', p4a.subtyper)
        import osha.policy
        zcml.load_config('configure.zcml', osha.policy)
        import osha.theme
        zcml.load_config('configure.zcml', osha.theme)
        import slc.shoppinglist
        zcml.load_config('configure.zcml', slc.shoppinglist)
        fiveconfigure.debug_mode = False

        browserlayerutils.register_layer(IOSHACommentsLayer, 'osha.policy')
        SiteLayer.setUp()


class OshaThemeTestCase(ptc.PloneTestCase):
    """Base class for integration tests for the 'OshaTheme' product.
    """
    layer = OshaThemeLayer


class OshaThemeFunctionalTestCase(ptc.FunctionalTestCase):
    """Base class for functional integration tests for the 'OshaTheme' product.
    """
    layer = OshaThemeLayer

    def getBrowser(self, url):
        browser = Browser()
        browser.open(url)
        browser.getControl(name='__ac_name').value = portal_owner
        browser.getControl(name='__ac_password').value = default_password
        browser.getControl(name='submit').click()
        return browser

    def loadfile(self, rel_filename):
        home = package_home(product_globals)
        filename = os.path.sep.join([home, rel_filename])
        data = StringIO(open(filename, 'r').read())
        data.filename = os.path.basename(rel_filename)
        return data


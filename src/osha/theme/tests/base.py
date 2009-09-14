import os
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from StringIO import StringIO
from Globals import package_home
from osha.theme.config import product_globals

# Let Zope know about the two products we require above-and-beyond a basic
# Plone install (PloneTestCase takes care of these).
# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Products.PloneTestCase.layer import onsetup, PloneSite
from Products.PloneTestCase import layer

SiteLayer = layer.PloneSite

class OshaThemeLayer(SiteLayer):
    @classmethod
    def setUp(cls):
        ztc.installProduct('PloneLanguageTool')
        ztc.installProduct('LinguaPlone')
        ztc.installProduct('SimpleAttachment')
        ztc.installProduct('RichDocument')
        ztc.installProduct('PlacelessTranslationService')

        setupPloneSite(products=[
                                'osha.theme',
                                'SimpleAttachment',
                                'RichDocument',
                                'LinguaPlone'])
        import Products.PlacelessTranslationService
        import osha.theme
        zcml.load_config('configure.zcml', Products.PlacelessTranslationService)
        zcml.load_config('configure.zcml', osha.theme)
        fiveconfigure.debug_mode = False
        ztc.installPackage('Products.PlacelessTranslationService', quiet=True)
        ztc.installPackage('osha.theme')
        SiteLayer.setUp()

class OshaThemeTestCase(PloneTestCase):
    """Base class for integration tests for the 'OshaTheme' product.
    """
    layer = OshaThemeLayer

class OshaThemeFunctionalTestCase(FunctionalTestCase):
    """Base class for functional integration tests for the 'OshaTheme' product.
    """
    layer = OshaThemeLayer

    def loadfile(self, rel_filename):
        home = package_home(product_globals)
        filename = os.path.sep.join([home, rel_filename])
        data = StringIO(open(filename, 'r').read())
        data.filename = os.path.basename(rel_filename)
        return data

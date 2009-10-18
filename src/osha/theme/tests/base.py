from StringIO import StringIO
import os

from Globals import package_home
from Products.Five import fiveconfigure
from Products.Five import zcml
from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import layer
from Products.PloneTestCase.layer import onsetup, PloneSite
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite

from plone.browserlayer import utils as browserlayerutils
from osha.policy.interfaces import IOSHACommentsLayer

from osha.theme.config import product_globals

SiteLayer = layer.PloneSite

class OshaThemeLayer(SiteLayer):
    @classmethod
    def setUp(cls):
        """
        The osha.theme package depends on osha.policy so the packages imported
        by the osha.policy tests base.py are also imported and configured here.
        """
        ztc.installProduct('PloneLanguageTool')
        ztc.installProduct('LinguaPlone')
        ztc.installProduct('SimpleAttachment')
        ztc.installProduct('RichDocument')
        ztc.installProduct('PlacelessTranslationService')
        ztc.installPackage('osha.policy')
        ztc.installPackage('p4a.plonevideoembed')
        setupPloneSite(products=[
                                'slc.shoppinglist',
                                'CMFLinkChecker',
                                'LinguaPlone',
                                'slc.linguatools',
                                'osha.policy',
                                'osha.theme',
                                'p4a.subtyper',
                                'p4a.plonevideoembed',
                                'RichDocument',
                                'SimpleAttachment',
                                ])
        import Products.PlacelessTranslationService
        import osha.theme
        import osha.policy
        import p4a.subtyper
        import slc.shoppinglist
        import slc.linguatools

        # osha.policy related products:
        ztc.installPackage('osha.legislation')
        ztc.installPackage('slc.seminarportal')
        ztc.installPackage('slc.alertservice')
        ztc.installPackage('slc.linguatools')
        ztc.installProduct('ATCountryWidget')
        ztc.installProduct('ATVocabularyManager')
        ztc.installProduct('LinguaPlone')
        ztc.installProduct('ProxyIndex')
        ztc.installProduct('Relations')
        ztc.installProduct('TextIndexNG3')

        zcml.load_config('configure.zcml', Products.PlacelessTranslationService)
        zcml.load_config('configure.zcml', osha.theme)
        zcml.load_config('configure.zcml', osha.policy)
        zcml.load_config('configure.zcml', p4a.subtyper)
        zcml.load_config('configure.zcml', slc.shoppinglist)
        zcml.load_config('configure.zcml', slc.linguatools)
        zcml.load_config('configure.zcml', p4a.plonevideoembed)
        fiveconfigure.debug_mode = False
        ztc.installPackage('Products.PlacelessTranslationService', quiet=True)
        ztc.installPackage('osha.theme')
        ztc.installPackage('osha.policy')
        ztc.installPackage('slc.shoppinglist')
        ztc.installPackage('p4a.subtyper')
        ztc.installPackage('p4a.plonevideoembed')
        # register the Browserlayer from osha.policy, so that our schema-extensions
        # using IBrowserLayerAwareExtender work
        browserlayerutils.register_layer(IOSHACommentsLayer, 'osha.policy')
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

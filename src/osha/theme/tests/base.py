import os
from Globals import package_home
from StringIO import StringIO
from Testing import ZopeTestCase as ztc

from plone.browserlayer import utils as browserlayerutils

from Products.PloneTestCase import layer
import Products.LinguaPlone
# # importing LinguaPlone to avoid a problem with circular imports
# # See http://do3cc.blogspot.com/2010/08/dont-catch-import-errors-use.html
# # The problem begins here:
# # Products/PloneTestCase/setup.py:
# # ZopeTestCase.installProduct('CMFPlone', quiet=1)
from Products.PloneTestCase import PloneTestCase as ptc

from osha.policy.interfaces import IOSHACommentsLayer
from osha.theme.config import product_globals


SiteLayer = layer.PloneSite

class OshaThemeLayer(SiteLayer):

    @classmethod
    def setUp(cls):
        """ The osha.theme package depends on osha.policy so the packages imported
            by the osha.policy tests base.py are also imported and configured here.
        """

        ztc.installProduct('ATCountryWidget')
        ztc.installProduct('ATVocabularyManager')
        ztc.installProduct('LinguaPlone')
        ztc.installProduct('ProxyIndex')
        ztc.installProduct('Relations')
        ztc.installProduct('TextIndexNG3')

        ztc.installPackage('osha.legislation')

        PRODUCTS = [
                'osha.policy',
                ]
        ptc.setupPloneSite(products=PRODUCTS)
        browserlayerutils.register_layer(IOSHACommentsLayer, 'osha.policy')
        SiteLayer.setUp()

        # import Products.PlacelessTranslationService
        # import osha.policy
        # import osha.theme
        # import p4a.subtyper
        # import slc.linguatools
        # import slc.shoppinglist

        # ztc.installProduct('PloneLanguageTool')
        # ztc.installProduct('LinguaPlone')
        # ztc.installProduct('SimpleAttachment')
        # ztc.installProduct('RichDocument')
        # ztc.installProduct('PlacelessTranslationService')
        # ptc.setupPloneSite(products=[
        #                         'slc.shoppinglist',
        #                         'CMFLinkChecker',
        #                         'LinguaPlone',
        #                         'slc.linguatools',
        #                         'osha.policy',
        #                         'osha.theme',
        #                         'RichDocument',
        #                         'SimpleAttachment',
        #                         ])

        # # osha.policy related products:
        # ztc.installPackage('slc.seminarportal')
        # ztc.installPackage('slc.alertservice')
        # ztc.installPackage('slc.linguatools')
        # ztc.installProduct('ATCountryWidget')
        # ztc.installProduct('ATVocabularyManager')
        # ztc.installProduct('LinguaPlone')
        # ztc.installProduct('ProxyIndex')
        # ztc.installProduct('Relations')
        # ztc.installProduct('TextIndexNG3')

        # zcml.load_config('configure.zcml', Products.LinguaPlone)
        # zcml.load_config('configure.zcml', Products.PlacelessTranslationService)
        # zcml.load_config('configure.zcml', osha.theme)
        # zcml.load_config('configure.zcml', osha.policy)
        # zcml.load_config('configure.zcml', p4a.subtyper)
        # zcml.load_config('configure.zcml', slc.shoppinglist)
        # zcml.load_config('configure.zcml', slc.linguatools)

        # fiveconfigure.debug_mode = False

        # ztc.installPackage('Products.PlacelessTranslationService', quiet=True)
        # ztc.installPackage('osha.policy')
        # ztc.installPackage('osha.policy')
        # ztc.installPackage('osha.theme')
        # ztc.installPackage('p4a.subtyper')
        # ztc.installPackage('slc.shoppinglist')

        # register the Browserlayer from osha.policy, so that our schema-extensions
        # using IBrowserLayerAwareExtender work


class OshaThemeTestCase(ptc.PloneTestCase):
    """Base class for integration tests for the 'OshaTheme' product.
    """
    layer = OshaThemeLayer


class OshaThemeFunctionalTestCase(ptc.FunctionalTestCase):
    """Base class for functional integration tests for the 'OshaTheme' product.
    """
    layer = OshaThemeLayer

    def loadfile(self, rel_filename):
        home = package_home(product_globals)
        filename = os.path.sep.join([home, rel_filename])
        data = StringIO(open(filename, 'r').read())
        data.filename = os.path.basename(rel_filename)
        return data


import os
from Globals import package_home
from StringIO import StringIO
from Testing import ZopeTestCase as ztc

from plone.browserlayer import utils as browserlayerutils

# # importing LinguaPlone to avoid a problem with circular imports
# # See http://do3cc.blogspot.com/2010/08/dont-catch-import-errors-use.html
# # The problem begins here:
# # Products/PloneTestCase/setup.py:
# # ZopeTestCase.installProduct('CMFPlone', quiet=1)
import Products.LinguaPlone

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import layer
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
        ztc.installProduct('PlacelessTranslationService')
        ztc.installProduct('PloneLanguageTool')
        ztc.installProduct('ProxyIndex')
        ztc.installProduct('Relations')
        ztc.installProduct('RichDocument')
        ztc.installProduct('SimpleAttachment')
        ztc.installProduct('TextIndexNG3')

        ztc.installPackage('Products.PlacelessTranslationService', quiet=True)
        ztc.installPackage('osha.legislation')
        ztc.installPackage('osha.policy')
        ztc.installPackage('osha.theme')
        ztc.installPackage('slc.seminarportal')
        ztc.installPackage('slc.shoppinglist')

        PRODUCTS = [
                'osha.policy',
                ]
        ptc.setupPloneSite(products=PRODUCTS)

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

    def loadfile(self, rel_filename):
        home = package_home(product_globals)
        filename = os.path.sep.join([home, rel_filename])
        data = StringIO(open(filename, 'r').read())
        data.filename = os.path.basename(rel_filename)
        return data


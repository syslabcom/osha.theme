from persistent.dict import PersistentDict
from Products.CMFCore.utils import getToolByName
from Products.ResourceRegistries.exportimport.resourceregistry import \
    importResRegistry
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from zope.component import getUtility


def guard(func):
    def wrapper(context):
        if context.readDataFile('osha.theme_various.txt') is None:
            return
        return func(context)
    return wrapper


def helpViewletManager(portal):
    """Viewlet storage works only for skins that have been hidden once before.
    With this we perform a kind of registration for skins.
    """
    portal_skins = getToolByName(portal, 'portal_skins')
    skins = portal_skins.getSkinSelections()
    storage = getUtility(IViewletSettingsStorage)

    for skin in skins:
        storage._hidden.setdefault(skin, PersistentDict())


@guard
def setupVarious(context):
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    portal = context.getSite()
    helpViewletManager(portal)


@guard
def resetCSSRegistry(context):
    """Remove all resources from the Css registry and add them from
    cssregistry.xml
    """
    portal = context.getSite()
    portal_css = getToolByName(portal, 'portal_css')
    portal_css.clearResources()

    return importResRegistry(
        context,
        'portal_css',
        'OSHA Css registry',
        'cssregistry.xml'
    )

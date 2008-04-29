from zope.component import getUtility
from zope.component import getMultiAdapter
from persistent.dict import PersistentDict
from plone.app.viewletmanager.interfaces import IViewletSettingsStorage
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from Products.CMFCore.utils import getToolByName

from osha.theme import portlets


def helpViewletManager(portal):
    """ Viewlet storage works only for skins that have been hidden once before
        With this we perform a kind of registration for skins
    """        
    portal_skins = getToolByName(portal, 'portal_skins')
    skins = portal_skins.getSkinSelections()
    
    storage = getUtility(IViewletSettingsStorage)
    
    for skin in skins:
        storage._hidden.setdefault(skin, PersistentDict())

def setupVarious(context):
    
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a 
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    
    if context.readDataFile('osha.theme_various.txt') is None:
        return
                
    portal = context.getSite()
    helpViewletManager(portal)


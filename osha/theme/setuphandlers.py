from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager

from osha.theme import portlets

def setupVarious(context):
    
    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a 
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.
    
    if context.readDataFile('osha.theme_various.txt') is None:
        return
                
    portal = context.getSite()
    assignPortlets(portal)
        
def assignPortlets(portal):
    rightColumn = getUtility(IPortletManager, name=u'plone.rightcolumn',
            context=portal)
    
    right = getMultiAdapter((portal, rightColumn,), IPortletAssignmentMapping,
            context=portal)                 

    if u'alertservice' not in right:
        right[u'alertservice'] = portlets.alertservice.Assignment()
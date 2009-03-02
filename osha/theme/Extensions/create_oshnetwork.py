from zope.app.container.interfaces import INameChooser

from zope.component import getUtility, getMultiAdapter

from plone.app.contentrules.rule import Rule
from plone.app.portlets.interfaces import ILeftColumn, IRightColumn
from plone.app.portlets.storage import PortletAssignmentMapping 
from plone.app.portlets.portlets import classic, events, news

from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction

from plone.portlets.interfaces import IPortletType 
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.constants import CONTEXT_CATEGORY as CONTEXT_PORTLETS

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from StringIO import StringIO

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.SEPStructure.util import addContentRule, assignRuleToObject

from osha.theme.config import EUROPEAN_NETWORK

def run(self):
    """ - Create folder called oshnetwork (inside 'en' folder). DONE
        - Add a subfolder per country  DONE
        - Add an empty index page. DONE
        - Implement the country dropdown (classic portlet) DONE
        - Block the portlets DONE
        - Content rule (on publish) for news and events added to the FOP DONE
        - Reuse the document_view to created oshnetwork_view
          folder.
    """
    createContentRules(self) 
    createOSHNetworkFolder(self)
    createCountrySubfolders(self)
    createClassicPortletWithCountryDropdown(self)
    blockPortlets(self)
    addExternalPortlet(self)
    addEventsAndNewsPortlets(self)
    return 'Finished!'

def getParent(self):
    portal = getToolByName(self, 'portal_url').getPortalObject()
    if hasattr(portal, 'en'):
        parent = getattr(portal, 'en')
    else:
        # XXX: Assuming for now we're on a test instance.
        # return "Portal has no folder with id 'en', operation aborted."
        parent = portal
    return parent


def createContentRules(self):
    """ """
    portal = getToolByName(self, 'portal_url').getPortalObject()
    rule_id = 'move-news-after-publish'
    addContentRule(
        context     = portal, 
        rule_id     = rule_id, 
        title       = u'Move published news items to /news folder', 
        description = u'This rule moves all objects of type NewsItem to the news folder in the site root.', 
        eventID     = u'Workflow state changed', 
        conditions  = (
            ('plone.conditions.PortalType', {'check_types' : ['News Item']}),
            ('plone.conditions.WorkflowState', {'wf_states' : ['published']}),
            ), 
        actions     = (('plone.actions.Move', {'target_folder' : '/news'}),)
        )
                      
    rule_id = 'move-events-after-publish'
    addContentRule(
        context     = portal, 
        rule_id     = rule_id, 
        title       = u'Move published event items to /events folder', 
        description = u'This rule moves all objects of type ATEvent to the events folder in the site root.', 
        eventID     = u'Workflow state changed', 
        conditions  = (
            ('plone.conditions.PortalType', {'check_types' : ['Event']}),
            ('plone.conditions.WorkflowState', {'wf_states' : ['published']}),
            ),
        actions     = (('plone.actions.Move', {'target_folder' : '/events'}),),
        )

def createOSHNetworkFolder(self):
    """ """
    parent = getParent(self)
    # Create oshnetwork folder and publish it.
    if not hasattr(parent, 'oshnetwork'):
        title = 'OSHNetwork'
        desc = 'The OSHNetwork folder contains the focal points (FOPs) for \
        all countries associated with OSHA'
        parent.invokeFactory('Folder', 
                            'oshnetwork', 
                            title=title,
                            description=desc)

    oshnetwork = getattr(parent, 'oshnetwork')
    wftool = getToolByName(self, 'portal_workflow')
    wftool.doActionFor(oshnetwork, 'publish')

    oshnetwork.invokeFactory('Document', 'index.html')
    document = getattr(oshnetwork, 'index.html')
    document.setTitle('OSHNetwork')
    document._setProperty('layout', 'oshnetwork_country_view')
    wftool.doActionFor(document, 'publish')

def createCountrySubfolders(self):
    """ Create subfolder with index.hml in each country folder
    """
    wftool = getToolByName(self, 'portal_workflow')
    parent = getParent(self)
    oshnetwork = getattr(parent, 'oshnetwork')
    for cc_and_name, link in EUROPEAN_NETWORK:
        try:
            cc, name = cc_and_name.split(' ', 1)
        except ValueError:
            # Account for country group delimiters
            continue

        # XXX: For now only create UK, DE and DK
        if cc not in ['UK', 'DE', 'DK']:
            continue
        
        if not hasattr(oshnetwork, name.lower()):
            oshnetwork.invokeFactory('Folder', name.lower().replace(' ','-'), title=name)

        folder = getattr(oshnetwork, cc)
        wftool.doActionFor(folder, 'publish')

        for rule_id in ['move-news-after-publish', 
                        'move-events-after-publish']:
            assignRuleToObject(context=folder, 
                               rule_id = rule_id, 
                               bubbles=True)

        folder.invokeFactory('Document', 'index.html')
        document = getattr(folder, 'index.html')
        document.setTitle(name)
        wftool.doActionFor(document, 'publish')

def blockPortlets(self):
    """ Block the showing of portlets in oshnetwork
    """
    parent = getParent(self)
    obj = getattr(parent, 'oshnetwork')
    for cname in ['plone.rightcolumn', 'plone.leftcolumn']:
        column = getUtility(IPortletManager, name=cname)
        ptass = getMultiAdapter((obj, column,), ILocalPortletAssignmentManager)
        ptass.setBlacklistStatus(CONTEXT_PORTLETS, True)

def addEventsAndNewsPortlets(self):
    """ """
    parent = getParent(self)
    obj = getattr(parent, 'oshnetwork')
    column = getUtility(IPortletManager, name='plone.leftcolumn')
    manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
    assignment = events.Assignment()
    chooser = INameChooser(manager)
    manager[chooser.chooseName(None, assignment)] = assignment

    column = getUtility(IPortletManager, name='plone.rightcolumn')
    manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
    assignment = news.Assignment()
    chooser = INameChooser(manager)
    manager[chooser.chooseName(None, assignment)] = assignment

def createClassicPortletWithCountryDropdown(self):
    """ """
    parent = getParent(self)
    obj = getattr(parent, 'oshnetwork')
    column = getUtility(IPortletManager, name='plone.leftcolumn')
    manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
    assignment = classic.Assignment(template='oshnetwork_country_select',
                                    macro='portlet')
    chooser = INameChooser(manager)
    manager[chooser.chooseName(None, assignment)] = assignment

def addExternalPortlet(self):
    """ """
    parent = getParent(self)
    obj = getattr(parent, 'oshnetwork')
    column = getUtility(IPortletManager, name='plone.rightcolumn')
    manager = getMultiAdapter((obj, column,), IPortletAssignmentMapping)
    assignment = classic.Assignment(template='oshnetwork_external_links_portlet',
                                    macro='portlet')
    chooser = INameChooser(manager)
    manager[chooser.chooseName(None, assignment)] = assignment



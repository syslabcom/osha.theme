from StringIO import StringIO
import logging

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from Acquisition import aq_parent
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.SEPStructure.util import addContentRule, assignRuleToObject
from plone.app.contentrules.rule import Rule
from plone.app.portlets.interfaces import ILeftColumn, IRightColumn
from plone.app.portlets.portlets import classic, events, news
from plone.app.portlets.storage import PortletAssignmentMapping 
from plone.contentrules.engine.interfaces import IRuleStorage
from plone.contentrules.rule.interfaces import IRuleAction
from plone.portlets.constants import CONTEXT_CATEGORY as CONTEXT_PORTLETS
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletType 
from zope.app.container.interfaces import INameChooser
from zope.component import getUtility, getMultiAdapter

from osha.theme.config import EUROPEAN_NETWORK

COUNTRY_LANGS = {'romania': [('en', u'English'), ('ro', u'Romanian')],
                'united-kingdom': [('en', u'English')],
                'estonia': [('en', u'English'), ('et', u'Estonian')],
                'austria': [('de', u'German')],
                'greece': [('en', u'English'), ('el', u'Greek')],
                'hungary': [('en', u'English'), ('hu', u'Hungarian')],
                'cyprus': [('en', u'English'), ('el', u'Greek')],
                'turkey': [('en', u'English'), ('tr', u'Turkish')],
                'eu-us': [('en', u'English')],
                'mecklenburg-vorpommern': [('de', u'German')],
                'italy': [('en', u'English'), ('it', u'Italian')],
                'portugal': [('en', u'English'), ('pt', u'Portuguese')],
                'lithuania': [('en', u'English'), ('lt', u'Lithuanian')],
                'malta': [('en', u'English')],
                'france': [('fr', u'French')],
                'slovakia': [('en', u'English'), ('sk', u'Slovak')],
                'ireland': [('en', u'English')],
                'thueringen': [('de', u'German')],
                'norway': [('en', u'English'), ('no', u'Norwegian')],
                'luxemburg': [('fr', u'French')],
                'sachsen-anhalt': [('de', u'German')],
                'korea': [('en', u'English'), ('ko', u'Korean')],
                'slovenia': [('en', u'English'), ('sl', u'Slovenian')],
                'germany': [('en', u'English'), ('de', u'German')],
                'belgium': [('nl', u'Dutch'), ('fr', u'French')],
                'bayern': [('de', u'German')],
                'rheinland-pfalz': [('de', u'German')],
                'spain': [('en', u'English'), ('es', u'Spanish')],
                'netherlands': [('nl', u'Dutch'), ('en', u'English')],
                'denmark': [('da', u'Danish'), ('en', u'English')],
                'poland': [('en', u'English'), ('pl', u'Polish')],
                'finland': [('en', u'English'), ('fi', u'Finnish'), ('sv', u'Swedish')],
                'sweden': [('en', u'English')],
                'latvia': [('en', u'English'), ('lv', u'Latvian')],
                'croatia': [('hr', u'Croatian'), ('en', u'English')],
                'uems': [('en', u'English')],
                'switzerland': [('en', u'English'), ('fr', u'French'), ('de', u'German'), ('it', u'Italian')],
                'czech-republic': [('cs', u'Czech'), ('en', u'English')],
                'bulgaria': [('bg', u'Bulgarian'), ('en', u'English')]}

MEMBER_STATES = [
    "Belgium",
    "Bulgaria",
    "Czech Republic",
    "Denmark",
    "Germany",
    "Estonia",
    "Ireland",
    "Greece",
    "Spain",
    "France",
    "Italy",
    "Cyprus",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Hungary",
    "Malta",
    "Netherlands",
    "Austria",
    "Poland",
    "Portugal",
    "Romania",
    "Slovenia",
    "Slovakia",
    "Finland",
    "Sweden",
    "United Kingdom",
    "Iceland",
    "Liechtenstein",
    "Norway",
    "Switzerland",
    "Croatia",
    "The former Yugoslav Republic of Macedonia",
    "Turkey",
    "Albania",
    "Bosnia and Herzegovina",
    "Kosovo under UNSCR 1244/99",
    "Montenegro",
    "Serbia",
    ]


# Unless already present use English(?)
not_present_on_current_site = ['luxembourg',
    'iceland',
    'liechtenstein',
    'the-former-yugoslav-republic-of-macedonia',
    'albania',
    'bosnia-and-herzegovina',
    'kosovo-under-unscr-1244/99',
    'montenegro',
    'serbia'
    ]



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
    createCountryFolder(self)   
    

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
    #import pdb; pdb.set_trace()
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
    # wftool = getToolByNamme(self, 'portal_workflow')
    # wftool.doActionFor(oshnetwork, 'publish')

    oshnetwork.invokeFactory('Document', 'index.html')
    document = getattr(oshnetwork, 'index.html')
    document.setTitle('OSHNetwork')
    document._setProperty('layout', 'oshnetwork-member-view')
    # wftool.doActionFor(document, 'publish')

def createCountrySubfolders(self):
    """ Create subfolder with index.hml in each country folder
    """
    wftool = getToolByName(self, 'portal_workflow')
    parent = getParent(self)
    # oshnetwork = getattr(parent, 'oshnetwork')
    oshnetwork = getattr(parent, 'OSHA')
    for cc_and_name, link in EUROPEAN_NETWORK:
        try:
            cc, name = cc_and_name.split(' ', 1)
        except ValueError:
            # Account for country group delimiters
            continue

        # XXX: For now only create UK, DE and DK
        if cc not in ['UK', 'DE', 'DK']:
            continue
        
        cid = name.lower().replace(' ','-')
        if not hasattr(oshnetwork, name.lower()):
            oshnetwork.invokeFactory('Folder', cid, title=name)

        folder = getattr(oshnetwork, cid)
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



from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter, queryUtility
from plone.app.portlets.portlets import navigation
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from zope import schema
from zope.formlib import form
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

class IInlineNavigationPortlet(IPortletDataProvider):
    """A portlet which can render the navigation tree
    """    
    
    name = schema.TextLine(
            title=_(u"label_navigation_title", default=u"Title"),
            description=_(u"help_navigation_title",
                          default=u"The title of the navigation tree. Leave "
                                   "blank for the default, translated title."),
            default=u"",
            required=False)
    
#    root = schema.Choice(
#            title=_(u"label_navigation_root_path", default=u"Root node"),
#            description=_(u'help_navigation_root',
#                          default=u"You may search for and choose a folder "
#                                    "to act as the root of the navigation tree. "
#                                    "Leave blank to use the Plone site root."),
#            required=False,
#            source=SearchableTextSourceBinder({'is_folderish' : True},
#                                              default_query='path:'))
                            
#    includeTop = schema.Bool(
#            title=_(u"label_include_top_node", default=u"Include top node"),
#            description=_(u"help_include_top_node",
#                          default=u"Whether or not to show the top, or 'root', "
#                                   "node in the navigation tree. This is affected " 
#                                   "by the 'Start level' setting."),
#            default=False,
#            required=False)
            
#    currentFolderOnly = schema.Bool(
#            title=_(u"label_current_folder_only",
#                    default=u"Only show the contents of the current folder."),
#            description=_(u"help_current_folder_only",
#                          default=u"If selected, the navigation tree will "
#                                   "only show the current folder and its "
#                                   "children at all times."),
#            default=True,
#            required=False)
    
#    topLevel = schema.Int(
#            title=_(u"label_navigation_startlevel", default=u"Start level"),
#            description=_(u"help_navigation_start_level",
#                default=u"An integer value that specifies the number of folder "
#                         "levels below the site root that must be exceeded "
#                         "before the navigation tree will display. 0 means "
#                         "that the navigation tree should be displayed "
#                         "everywhere including pages in the root of the site. "
#                         "1 means the tree only shows up inside folders "
#                         "located in the root and downwards, never showing "
#                         "at the top level."),
#            default=1,
#            required=False)
#    
#    bottomLevel = schema.Int(
#            title=_(u"label_navigation_tree_depth",
#                    default=u"Navigation tree depth"),
#            description=_(u"help_navigation_tree_depth",
#                          default=u"How many folders should be included "
#                                   "before the navigation tree stops. 0 "
#                                   "means no limit. 1 only includes the "
#                                   "root folder."),
#            default=0,
#            required=False)
            
class Assignment(base.Assignment):
    implements(IInlineNavigationPortlet)

    title = _(u'Inline Navigation')
    
    name = u""
    root = None
    currentFolderOnly = True
    includeTop = False
    topLevel = 1
    bottomLevel = 0
    
    def __init__(self, name=u"", root=None, currentFolderOnly=True, includeTop=False, topLevel=1, bottomLevel=0):
        self.name = name
        self.root = root
        self.currentFolderOnly = currentFolderOnly
        self.includeTop = includeTop
        self.topLevel = topLevel
        self.bottomLevel = bottomLevel
    
class Renderer(navigation.Renderer):
    """ displays the current navigation level in two columns under the body
        if enabled
    """
    _template = ViewPageTemplateFile('inline_navigation.pt')



    
class AddForm(base.AddForm):
    form_fields = form.Fields(IInlineNavigationPortlet)
    #form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Add Inline Navigation Portlet")
    description = _(u"This portlet display an inline navigation tree.")

    def create(self, data):
        return Assignment(name=data.get('name', u""),
                          root=data.get('root', u""),
                          currentFolderOnly=data.get('currentFolderOnly', True),
                          includeTop=data.get('includeTop', False),
                          topLevel=data.get('topLevel', 0),
                          bottomLevel=data.get('bottomLevel', 0))

class EditForm(base.EditForm):
    form_fields = form.Fields(IInlineNavigationPortlet)
    #form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Edit Inline Navigation Portlet")
    description = _(u"This portlet display an inline navigation tree.")    
    
    

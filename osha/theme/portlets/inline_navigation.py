from zope.interface import implements, Interface
from zope.component import adapts, getMultiAdapter, queryUtility
from plone.app.portlets.portlets import navigation
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone import PloneMessageFactory as _
from zope import schema
from zope.formlib import form

class IInlineNavigationPortlet(navigation.INavigationPortlet):
    """A portlet which can render the navigation tree
    """    

class Assignment(navigation.Assignment):
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



    
class AddForm(navigation.AddForm):
    form_fields = form.Fields(IInlineNavigationPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Add Inline Navigation Portlet")
    description = _(u"This portlet display an inline navigation tree.")

    def create(self, data):
        return Assignment(name=data.get('name', u""),
                          root=data.get('root', u""),
                          currentFolderOnly=data.get('currentFolderOnly', True),
                          includeTop=data.get('includeTop', False),
                          topLevel=data.get('topLevel', 0),
                          bottomLevel=data.get('bottomLevel', 0))

class EditForm(navigation.EditForm):
    form_fields = form.Fields(IInlineNavigationPortlet)
    form_fields['root'].custom_widget = UberSelectionWidget
    label = _(u"Edit Inline Navigation Portlet")
    description = _(u"This portlet display an inline navigation tree.")    

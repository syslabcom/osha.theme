from zope.formlib import form
from zope.interface import implements
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from osha.theme.portlets import practical_solutions as ps

class IPublicationsPortlet(ps.IPracticalSolutionsPortlet):
    """ """

class Assignment(ps.Assignment):
    implements(IPublicationsPortlet)

    def __init__(self, subject):
        self.subject = subject

    @property
    def title(self):
        return "Publications"


class Renderer(ps.Renderer):
    _template = ViewPageTemplateFile('publications.pt')


class AddForm(ps.AddForm):
    """ This is registered in configure.zcml. The form_fields variable tells
        zope.formlib which fields to display. The create() method actually
        constructs the assignment that is being added.
    """
    form_fields = form.Fields(IPublicationsPortlet)
    form_fields['subject'].custom_widget = ps.MultiCheckBoxWidgetFactory

    def create(self, data):
        return Assignment(**data)


class EditForm(ps.EditForm):
    """ This is registered with configure.zcml. The form_fields variable tells
        zope.formlib which fields to display.
    """
    form_fields = form.Fields(IPublicationsPortlet)
    form_fields['subject'].custom_widget  = ps.MultiCheckBoxWidgetFactory

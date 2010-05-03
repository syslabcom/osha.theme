from osha.theme.portlets.practical_solutions import Assignment, Renderer, \
    AddForm, EditForm, MultiCheckBoxWidgetFactory
from osha.theme.portlets.practical_solutions import IPracticalSolutionsPortlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.formlib import form
from zope.interface import implements


class IPublicationsPortlet(IPracticalSolutionsPortlet):
    """ nothing changed"""
    pass


class Assignment(Assignment):

    implements(IPublicationsPortlet)

    def __init__(self, subject):
        self.subject = subject

    @property
    def title(self):
        return "Publications"


class Renderer(Renderer):

    _template = ViewPageTemplateFile('publications.pt')



class AddForm(AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    form_fields = form.Fields(IPublicationsPortlet)
    form_fields['subject'].custom_widget  = MultiCheckBoxWidgetFactory

    def create(self, data):
        return Assignment(**data)


class EditForm(EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IPublicationsPortlet)
    form_fields['subject'].custom_widget  = MultiCheckBoxWidgetFactory

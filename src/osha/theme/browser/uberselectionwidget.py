from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget as BaseUberSelectionWidget
from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile

class UberSelectionWidget(BaseUberSelectionWidget):
    
    template = ViewPageTemplateFile('templates/uberselectionwidget.pt')
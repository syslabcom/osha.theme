from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements
from osha.theme.browser.interfaces import ICompetitionsView, ICompetitionDetail


class CompetitionsView(BrowserView):
    implements(ICompetitionsView)

    template = ViewPageTemplateFile('templates/competitions_view.pt')
    template.id = "competitions-view"

    def __call__(self):
        return self.template()


class CompetitionDetail(BrowserView):
    implements(ICompetitionDetail)

    template = ViewPageTemplateFile('templates/competition_detail.pt')
    template.id = "competition-detail"

    def __call__(self):
        return self.template()

from zope.interface import alsoProvides
from kss.core import kssaction
from plone.app.kss.plonekssview import PloneKSSView
from plone.app.layout.globals.interfaces import IViewView
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from osha.theme.browser.interfaces import IRollingQuotesToolsView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from DateTime import DateTime
import random
from Products.CMFCore.utils import getToolByName

class RollingQuotesToolsView(PloneKSSView):
    portlet_template=ViewPageTemplateFile('templates/rollingbody.pt')
    folderUrl=""
    folderob=None

    @kssaction
    def set_url(self, url):
        self.folderUrl=url

        alsoProvides(self, IViewView)
        ksscore = self.getCommandSet('core')
        zopecommands = self.getCommandSet('zope')
        plonecommands = self.getCommandSet('plone')
        selector = ksscore.getHtmlIdSelector('roll')
        ksscore.replaceHTML('.roll',self.portlet_template())

    def fallback(self, ob, preflang):
        if ob is None:
            return None
        pref = ob.getTranslation(preflang)
        if not pref:
            canonical = ob.getCanonical()   
            return canonical
        return pref

    def getDateTime(self):
        return str(self.folderUrl)

    def getRandomObject(self):
        portal_languages=getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()

        folderob=self.context.restrictedTraverse(self.folderUrl)
        folderlist = folderob.listFolderContents(contentFilter={"portal_type" : "News Item", "review_state": "published"})
        ob = random.choice(folderlist)
        ob = self.fallback(ob, preflang)
        return ob
        
    def get_url(self):
        return self.folderUrl

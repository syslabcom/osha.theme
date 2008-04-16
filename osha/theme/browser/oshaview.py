import Acquisition
from time import time
from osha.theme.browser.interfaces import IOSHA
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from zope.interface import implements, alsoProvides
from plone.memoize.instance import memoize
from plone.memoize import ram


class OSHA(BrowserView):
    implements(IOSHA)

    def cropHtmlText(self, text, length, ellipsis='...'):
        """ first strip html, then crop """
        context = Acquisition.aq_inner(self.context)
        portal_transforms = getToolByName(context, 'portal_transforms')
        text = portal_transforms.convert('html_to_text', text).getData()
        return context.restrictedTraverse('@@plone').cropText(text, length, ellipsis)
        
        
    @ram.cache(lambda *args: time() // (60 * 60))
    def getSingleEntryPoints(self):
        """ Retrieve all sections implementing ISubsite that match the local Subjects """
        portal_catalog = getToolByName(self, 'portal_catalog')
        sections = portal_catalog(object_provides='osha.policy.interfaces.ISingleEntryPoint', 
                                  review_state="published")
        rs = []
        for section in sections:
            rs.append(dict(title=section.Title, url=section.getURL(), subject=section.Subject ))
        rs.sort(lambda x,y: cmp(x['title'].lower(), y['title'].lower()))
        return rs        
        
    def getSingleEntryPointsBySubject(self, subjects):
        """ Retrieve all sections implementing ISubsite that match the local Subjects """
        seps = self.getSingleEntryPoints()
        
        seplist = []
        
        for sep in seps:
            S = sep['subject']
            for subject in S:
                if subject in subjects:
                    seplist.append(sep)
                    continue
                    
        seplist.sort(lambda x,y: cmp(x['title'].lower(), y['title'].lower()))
        return seplist     
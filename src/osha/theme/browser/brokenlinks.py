import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

class BrokenLinkLog(BrowserView):
    """View for displaying the broken links in PM format
    """
    template = ViewPageTemplateFile('templates/brokenlinks.pt')
    
    def __call__(self):
        self.request.set('disable_border', True)

        return self.template() 


    def broken_links(self):
        """ return all links sorted by path which need PM attention 
        """
        context = Acquisition.aq_inner(self.context)
        link_catalog = getToolByName(context, 'portal_linkchecker').database.link_catalog
        uid_catalog = getToolByName(context, 'uid_catalog')
        results = link_catalog(state=['red', 'orange'])
        links = []
        uids = []
        for link in results:
            item = {}
            item["url"] = link.url
            item["reason"] = link.reason
            item["lastcheck"] = link.lastcheck
            item["id"] = link.getId
            item["link"] = link.link
            item["state"] = link.state
            item["object"] = link.object
            links.append(item)
            ob = uid_catalog(UID=link.object)[0].getObject()
            item["document"] = ob
            item['path'] = ob.absolute_url()
            
        links.sort(lambda x,y: cmp(x['path'], y['path']))
        return links
        
        
   
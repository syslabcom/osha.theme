from Products.CMFCore.utils import getToolByName

from osha.theme.config import EUROPEAN_NETWORK

def custom_view(self):
    return self.oshnetwork_country_view()

def run(self):
    """ - Create folder called oshnetwork (inside 'en' folder).
        - Add a subfolder per country 
        - In the navigation portlet, move it below about.
        - Add and empty index page.
        - Block the portlets
        - Implement the country dropdown (classic portlet)
        - Reuse the document_view to created oshnetwork_view
        - Content rule (on publish) for news and events added to the FOP
          folder.
    """
    portal = getToolByName(self, 'portal_url').getPortalObject()

    if hasattr(portal, 'en'):
        parent = getattr(portal, 'en')
    else:
        # XXX: Assuming for now we're on a test instance.
        # return "Portal has no folder with id 'en', operation aborted."
        parent = portal

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
    wftool = getToolByName(self, 'portal_workflow')
    wftool.doActionFor(oshnetwork, 'publish')


    # Create subfolder with index.hml in each country folder
    for cc_and_name, link in EUROPEAN_NETWORK:
        try:
            cc, name = cc_and_name.split(' ', 1)
        except ValueError:
            # Account for country group delimiters
            continue

        # XXX: For now only create UK, DE and DK
        if cc not in ['UK', 'DE', 'DK']:
            continue
        
        if not hasattr(oshnetwork, name.lower()):
            oshnetwork.invokeFactory('Folder', name.lower(), title=name)
            folder = getattr(oshnetwork, name.lower())
            wftool.doActionFor(folder, 'publish')
            folder.invokeFactory('Document', 'index.html')
            document = getattr(folder, 'index.html')
            wftool.doActionFor(document, 'publish')
    
    return 'Sucessfully created'





            

    




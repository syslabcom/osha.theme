## Script (Python) "get_fop_countries"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Return the url of OSHNetwork folder.
##parameters=

portal = context.portal_url.getPortalObject()
if hasattr(portal, 'en'):
    parent = getattr(portal, 'en')
else:
    # XXX: Assuming for now we're on a test instance.
    # return "Portal has no folder with id 'en', operation aborted."
    parent = portal

if hasattr(parent, 'oshnetwork'):
    return parent.oshnetwork.absolute_url()

return ''


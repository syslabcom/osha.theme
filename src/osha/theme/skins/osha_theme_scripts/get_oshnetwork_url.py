## Script (Python) "get_fop_countries"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Return the url of OSHNetwork folder.
##parameters=


networkfolder = context
for i in context.REQUEST.PARENTS:
    if i.getId()=='oshnetwork':
        networkfolder = i

return networkfolder.absolute_url()


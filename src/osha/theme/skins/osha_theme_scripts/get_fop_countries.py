## Script (Python) "get_fop_countries"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Return a list of Focal Point Countries
##parameters=


networkfolder = context
for i in context.REQUEST.PARENTS:
    if i.getId()=='fopnetwork':
        networkfolder = i


countries = []
query = {
    'portal_type': 'Folder', 
    'sort_on': 'sortable_title', 
    'review_state': 'published',
    }
for item in networkfolder.getFolderContents(contentFilter=query):
    countries.append( (item.Title, item.getId) )

return countries


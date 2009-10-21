## Script (Python) "getContactFormUrl"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Return the url of the current subsite
##parameters=

pu = context.portal_url
purl = pu()
oshaview = context.restrictedTraverse('@@oshaview')
suburl = oshaview.subsiteRootUrl()
sub_path = oshaview.subsiteRootPath()
site = pu.restrictedTraverse(sub_path)

lang = context.portal_languages.getPreferredLanguage()
if not oshaview.isSubsite(site):
    template = 'contact_us'
else:
    template = 'contact-info'
    
return "%s/%s/%s" % (suburl, lang, template)

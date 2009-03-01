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
suburl = context.restrictedTraverse('@@oshaview').subsiteRootUrl()
lang = context.portal_languages.getPreferredLanguage()
if purl == suburl:
    template = 'contact_us'
else:
    template = 'contact-info'
    
return "%s/%s/%s" % (suburl, lang, template)

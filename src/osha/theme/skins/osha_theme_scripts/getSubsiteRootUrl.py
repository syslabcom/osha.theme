## Script (Python) "getSubsiteRootUrl"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=Return the url of the current subsite
##parameters=
return context.restrictedTraverse('@@oshaview').subsiteRootUrl()


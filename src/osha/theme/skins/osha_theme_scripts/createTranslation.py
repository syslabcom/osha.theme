## Script (Python) "creatTranslation"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##title=createTranslation
##parameters=set_language

""" 
The 'not_available_lang' form posts to createTranslation, which doesn't exits :-/
So we create it and forward to '@@translation?newlanguage=xx'.
"""
return context.REQUEST.RESPONSE.redirect('@@translate?newlanguage=%s' % set_language)

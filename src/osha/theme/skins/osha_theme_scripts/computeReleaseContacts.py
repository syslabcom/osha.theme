## Script (Python) "computeReleaseContacts"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=find press contacts for a press release
##

from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName

if hasattr(context, 'getReleaseContacts'):
    # XXX Syslab customization
    langtool = getToolByName(context, 'portal_languages')
    lang = langtool.getPreferredLanguage() 
    outgoing = [o.getTranslation(language=lang) or o.getCanonical() for o in context.getReleaseContacts()]
    # Here is the original:
    # outgoing = context.getReleaseContacts()

    incoming = []
    # if you want to show up the items which point to this one, too, then use the
    # line below
    #incoming = context.getBRefs('relatesTo') 
    res = []
    mtool = context.portal_membership
    
    in_out = outgoing+incoming
    for d in range(len(in_out)):
        try:
            obj = in_out[d]
        except Unauthorized:
            continue
        if obj not in res:
            if mtool.checkPermission('View', obj):
                res.append(obj)
    
    return res






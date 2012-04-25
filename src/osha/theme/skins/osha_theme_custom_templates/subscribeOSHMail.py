## Script (Python) "subscribeOSHMail"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=emailaddress='', noredirect=False
##title=subscribeOSHMail
##
""" helper method to enable osh mail subscription to anonymous user """
from Products.CMFCore.utils import getToolByName
from slc.alertservice import AlertMessageFactory as _

ptool = getToolByName(context, 'portal_url')
portal = ptool.getPortalObject()
pp = getToolByName(portal, 'portal_properties')
op = getattr(pp, 'osha_properties', None)
siteadmin = getattr(portal, 'email_from_address')
reg_tool = getToolByName(context, 'portal_registration')

REQUEST = context.REQUEST
if not emailaddress:
    emailaddress = REQUEST.get('emailaddress', '')
refererstem = REQUEST.get('HTTP_REFERER').split('?')[0]
referer = refererstem + '?'
qs = REQUEST.get('QUERY_STRING', '')
if qs:
    referer += '?' + qs + '&'

if reg_tool.isValidEmail(emailaddress):
    pass
else:
    msg = _(u'You did not enter a valid email address.')
    try:
        msg = unicode(msg, 'iso8859-1').encode('utf-8')
    except:
        pass
    return REQUEST.RESPONSE.redirect(referer + "portal_status_message=" + msg)


if REQUEST.get('submit') == 'unsubscribe':
    mesg = "UNSUBSCRIBE OSHMAIL\n"
    mssg = "Your unsubscription request has been sent."
else:
    mesg = "SUBSCRIBE OSHMAIL anonymous\n"
    mssg = "Your subscription request has been sent."


recipient = op.getProperty('listserv_email', siteadmin)

sender = emailaddress

subject = ''
try:
    context.MailHost.send(mesg , mto=recipient, mfrom=sender, subject=subject)
except Exception, e:
    mssg = "Your subscription could not be sent. Please try again."

if not noredirect:
    from slc.alertservice.utils import encodeEmail
    # this feedbackpage has been added to contain a specific tracking code for an external company
    #feedbackpage = "http://osha.europa.eu/news/oshmail/subscription_feedback?portal_status_message=%s&e=%s" % (mssg, encodeEmail(sender))
    return REQUEST.RESPONSE.redirect(refererstem + "/subscription_feedback?portal_status_message=%s&e=%s" % (mssg, encodeEmail(sender)))

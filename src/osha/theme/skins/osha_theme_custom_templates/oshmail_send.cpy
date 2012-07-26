## Controller Python Script "oshmail_send"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=email
##title=Send an OSHMail to the given email address

from logging import getLogger
log = getLogger("moah")

request = context.REQUEST

email_to = email
email_from = context.portal_properties.site_properties.email_from_address
from Products.CMFPlone.utils import getToolByName
host = getToolByName(context, 'MailHost')
email_subject = "%s\n" % (context.title_or_id())
email_body = context.oshmail_view()
oshaview = context.restrictedTraverse('@@oshaview')
inlinehtml = oshaview.inlinestyler(email_body)
email_body = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n'+inlinehtml

log.info(email_body)
    
err = host.send(email_body, mto=email_to, mfrom=email_from,
    subject=email_subject, msg_type='text/html', charset="utf-8")

if not err:
    return state.set(status='success', portal_status_message='The OSH Mail has been sent to the List Manager.')
else:
    return state.set(status='failure', portal_status_message='There was a problem sending the Shortmessage: ' + err)

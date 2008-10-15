## Controller Python Script "shortmessage_send"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=email
##title=Send a Shortmessage to the given email address

#from Products.Shortmessage.utils import sendShortmessage

request = context.REQUEST

email_to = email
email_from = context.portal_properties.site_properties.email_from_address
host = context.MailHost
email_subject = context.title_or_id()
email_body = context.shortmessage_preview_view()

err = host.secureSend(message=email_body, mto=email_to, mfrom=email_from, subject=email_subject, subtype="html", charset="utf-8")

if not err:
	return state.set(status='success', portal_status_message='The Shortmessage has been sent to the List Manager.')
else:
	return state.set(status='failure', portal_status_message='There was a problem sending the Shortmessage: ' + err)

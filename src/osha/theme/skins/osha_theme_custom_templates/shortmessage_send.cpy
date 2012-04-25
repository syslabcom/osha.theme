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

email_to_list = []
if email:
   email_to_list.append(email)
if request.form.has_key("email_groups"):
   # Can't pass in email_groups as a param, fails when empty
   email_groups = request.form["email_groups"]
   email_to_list.append(email_groups)

email_to = ",".join(email_to_list)
if not email_to:
   state.set(
      status='failure',
      portal_status_message="No email recipients have been specified")
   state.setError("email", "No email recipients have been specified",
                  new_status="failure")
   state.setError("email_groups", "No email recipients have been specified",
                  new_status="failure")
   return state

email_from = context.portal_properties.site_properties.email_from_address
host = context.MailHost
email_subject = context.title_or_id()
email_body = context.shortmessage_preview_view()

try:
   host.send(email_body, mto=email_to, mfrom=email_from, subject=email_subject,
             msg_type='text/html', charset="utf-8")
except Exception, msg:
   state.setError("email",
                  'There was a problem sending the Shortmessage: %s' % msg,
                  new_status="failure")
   return state

state.set(status='success',
          portal_status_message=('The Shortmessage has been sent to the '
                                 'List Manager.'))
return state

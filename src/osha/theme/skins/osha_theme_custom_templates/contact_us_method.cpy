## Controller Python Script "contact_us_method"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Send a comment to the agency
##
from Products.CMFCore.utils import getToolByName
request=context.REQUEST

portal_url = getToolByName(context, 'portal_url')
plone_utils = getToolByName(context, 'plone_utils')
ts = getToolByName(context, 'translation_service')
portal = portal_url.getPortalObject()

subject = request.get('subject', '')
sender = request.get('sender', '')
fullname = request.get('fullname', '')
country = request.get('country', '')
size_org = request.get('size_org', '')
name_org = request.get('name_org', '')
user_email = request.get('email', '')
message = request.get('message', '')
message = message.replace('\n', '<br>')
url_comment = request.get('url_comment', '')
url_broken = request.get('url_broken', '')
url_broken_location = request.get('url_broken_location', '')
url_new = request.get('url_new', '')

language = context.portal_languages.getPreferredLanguage()

            

if request.form.has_key('form.button.SenderSubject'):
                
    fields = {  'email': 1,
                'fullname': 1,
                'country': 1,
                'size_org': 1,
                'name_org' : 1,
                'message': 1,
                'url_comment': 0,
                'url_broken': 0,
                'url_broken_location': 0,
                'url_new': 0
            }

    
    
    if sender in ('Individual'
                  , 'Journalist'
                  , 'OSH practitioner'
                  , 'Researcher'
                  , 'Student' ):
        fields['size_org'] = 0
        fields['name_org'] = 0
        
    if subject in ('comments_web_content'
                   , 'comments_web_technical'):
        fields['url_comment'] = 1
        
    if subject in ('broken_link'):
        fields['url_broken'] = 1
        fields['url_broken_location'] = 1
        fields['url_new'] = 1

    if subject in ('interesting_link'):
        fields['url_new'] = 1


    request.set('fields', fields)
    return state.set(status='success_SenderSubject', request=request)
    
    
if request.form.has_key('form.button.Send'):    


    short_closing = ('broken_link'
                    , 'comments_web_content'
                    , 'comments_web_technical'
                    , 'interesting_link'
                    )

    obj = getattr(context.contact_data, subject, None)
    if obj is None:
        return state.set(status='failure', portal_status_message="Unknown subject.")

    intro_text = context.contact_data.misc.intro.getText()
    issue_text = obj.getText()
    if subject in short_closing:
        closing_text = context.contact_data.misc.ack_comment.getText()
        long_feedback = 0
    else:
        closing_text = context.contact_data.misc.ack_info.getText()
        long_feedback = 1

    request.set('long_feedback', long_feedback)

    # students always get the "nr 11" reply about "assistance with project (student)"
    if sender == "Student" and long_feedback:
        extraObj = getattr(context.contact_data, 'assistance', None)
        if extraObj is None:
            return state.set(status='failure', portal_status_message="Unknown extra subject.")
        extraIssue_text = subject!='assistance' and  extraObj.getText() or ""
        feedback_text = "%s\n%s\n%s\n%s" %(intro_text, extraIssue_text, issue_text, closing_text)
        request.set('student', 1)
        request.set('subject', subject)
    
    else:        
        feedback_text = "%s\n%s\n%s" %(intro_text, issue_text, closing_text)



    ## XXXX
    # Here's the shortcut:
    feedback_text = context.contact_data.misc.ack_standard.getText()

    
    from_address = portal.getProperty('email_from_address', 'comments@osha.europa.eu')

    context_state = context.restrictedTraverse("@@plone_context_state")
    url = context_state.view_url()


    title = obj.Title()

    oshaview = context.restrictedTraverse('@@oshaview')

    try:
        mail_text = oshaview.sendto( send_to_address=user_email
                                   , send_from_address=from_address
                                   , comment=feedback_text
                                   , title = "Feedback: %s " %title
                                   , subject="Feedback: %s " %title
                                   , subtype='html'
                                   , template = 'contact_feedback_template'
                                   , validate_to_address=0 )    
    except: # To many things could possibly go wrong. So we catch all.
        exception = context.plone_utils.exceptionString()
        message = ts.translate(u'Unable to send mail: ${exception}', domain="plone",
                    mapping={u'exception' : exception})
        context.plone_utils.addPortalMessage(message, 'error')
        return state.set(status='failure')


    if hasattr(context.aq_explicit, 'osha_properties'):
        osh_props = context.osha_properties 
    else:
        osh_props = context.portal_properties.osha_properties

    contact_us_mail_default = osh_props.getProperty('contact_us_mail_default')
    contact_us_mails_prop = osh_props.getProperty('contact_us_mails')

    contact_us_mails_map = {}
    for line in contact_us_mails_prop:
        try:
            k, v = line.split(':',1)
            contact_us_mails_map[k] = v
        except:
            pass

    if contact_us_mails_map.has_key(subject):
        send_to_address = contact_us_mails_map[subject]
    else:
        send_to_address = contact_us_mail_default     
    
    
    try:
        mail_text = oshaview.sendto( send_from_address=from_address
                                   , send_to_address=send_to_address
                                   , comment=message
                                   , title = title
                                   , subject = title
                                   , subtype='html'
                                   , email=user_email
                                   , template = 'contact_message_template'
                                   , validate_to_address=0
                                   , send_from_name=fullname
                                   , country = country
                                   , size_org = size_org
                                   , name_org = name_org
                                   , url_comment = url_comment
                                   , url_broken = url_broken
                                   , url_broken_location = url_broken_location
                                   , url_new = url_new
                                   , language = language
                                   , sender = sender
                 )    
    except: # TODO To many things could possibly go wrong. So we catch all.
        exception = context.plone_utils.exceptionString()
        message = ts.translate(u'Unable to send mail: ${exception}', domain="plone",
                     mapping={u'exception' : exception})
        context.plone_utils.addPortalMessage(message, 'error')
        return state.set(status='failure')

    
    return state.set(status='success_Send', request=request)
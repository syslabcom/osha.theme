## Controller Script Python "validate_contact_us"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=subject='',sender='', fullname='', email='', message=''
##title=validates 'contact us' data

request = context.REQUEST



if request.form.has_key('form.button.SenderSubject'):
    
    if subject=='':
        state.setError('subject', 'Please choose a subject.', 'input_required')
        
    if sender=='':
        state.setError('sender', 'Please select type of sender.', 'input_required')
    
    
        
    if state.getErrors():
        return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
    else:
        return state

if request.form.has_key('form.button.Send'):


    
    if fullname=='':
        state.setError('fullname', 'Please supply your name.', 'input_required')
        
    if email=='':
        state.setError('email', 'Please supply yor e-mail address.', 'input required')
        
    if message=='':
        state.setError('message', 'Please leave a short message.', 'input_required')
        
    if request.has_key('url_broken') and request.get('url_broken', '')=='':
        state.setError('url_broken', 'Please supply the URL of the broken link.', 'input_required')
        
    if request.has_key('url_broken_location') and request.get('url_broken_location', '')=='':
        state.setError('url_broken_location', 'Please supply the URL of the page wehre the broken link occured.', 'input_required')
        
        
    if state.getErrors():
        return state.set(status='failure', portal_status_message='Please correct the indicated errors.')
    else:
        return state
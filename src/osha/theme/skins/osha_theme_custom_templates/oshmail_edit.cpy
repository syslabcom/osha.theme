## Controller Python Script "oshmail_edit"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=color=''
##title=Edit a OSHMail Interface

request = context.REQUEST
if color.strip():
    if not context.hasProperty('color'):
        context.manage_addProperty('color', '#C5CBD8', 'string') 
    context.manage_changeProperties({'color': color})

            
if request.has_key('form.button.Config'):
    return state.set(status='success_Config', context=context , portal_status_message='Your Changes have been saved.')

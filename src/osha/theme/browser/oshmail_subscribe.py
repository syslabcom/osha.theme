from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView

from osha.theme import OSHAMessageFactory as _

class OSHmailSubscribe(BrowserView):
    """View for displaying oshmail
    """

    def __call__(self, emailaddress, name=''):

        """ helper method to enable osh mail subscription to anonymous user """
        ptool = getToolByName(self.context, 'portal_url')
        portal = ptool.getPortalObject()

        reg_tool = getToolByName(self.context, 'portal_registration')
        host = getToolByName(self.context, 'MailHost')

        REQUEST = self.request
        if not emailaddress:
            emailaddress = REQUEST.get('emailaddress', '')
        refererstem = REQUEST.get('HTTP_REFERER').split('?')[0]
        referer = refererstem + '?'
        qs = REQUEST.get('QUERY_STRING', '')
        if qs:
            referer += '?' + qs + '&'

        if not reg_tool.isValidEmail(emailaddress):
            msg = _(u'You did not enter a valid email address.')
            referer += "msg=%s&" % msg
            return REQUEST.RESPONSE.redirect(referer)

        if REQUEST.has_key('unsubscribe'):
            return REQUEST.RESPONSE.redirect(
                self.context.absolute_url() +
                "/confirm-unsubscription?emailaddress=%s" % (emailaddress))
        else:
            mesg = "subscribe OSHMail anonymous\n"
            mssg = _(
                "Thank you for subscribing to the OSHmail newsletter. You will "
                "receive an email to confirm your subscription.")


        recipient = 'listserv@list.osha.europa.eu'

        sender = emailaddress
        if name:
            sender = "%s <%s>" % (name, sender)

        subject = ''
        try:
            host.send(mesg, mto=recipient, mfrom=sender, subject=subject)
        except Exception, e:
            mssg = _("Your subscription could not be sent. Please try again.")
            mssg = u"%s %s" %(mssg, e)

        from slc.alertservice.utils import encodeEmail
        # this feedbackpage has been added to contain a specific
        # tracking code for an external company
        return REQUEST.RESPONSE.redirect(
            refererstem + "?e=%s&msg=%s" % (encodeEmail(sender), mssg))

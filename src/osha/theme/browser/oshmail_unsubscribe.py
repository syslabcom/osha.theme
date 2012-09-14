from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from slc.alertservice.utils import encodeEmail

from osha.theme import OSHAMessageFactory as _

class OSHmailUnsubscribe(BrowserView):
    """View for displaying oshmail
    """

    def __call__(self, confirm):

        """ helper method to enable osh mail subscription to anonymous user

        a tracking code is added to the response for tracking by an
        external company
        """
        ptool = getToolByName(self.context, 'portal_url')
        portal = ptool.getPortalObject()

        host = getToolByName(self.context, 'MailHost')
        REQUEST = self.request
        refererstem = REQUEST.get('HTTP_REFERER').split('?')[0]

        recipient = 'listserv@list.osha.europa.eu'
        sender = REQUEST.get('confirm_email')

        if confirm =='yes':
            mesg = "unsubscribe ICT-TEST\n"
            mssg = _("Thank you! You have been unsubscribed succesfully.")
            subject = ''
            try:
                host.send(mesg, mto=recipient, mfrom=sender, subject=subject)
            except Exception, e:
                mssg = _(
                    u"Your unsubscription request could not be sent. Please "
                    "try again.") + str(e)

            return REQUEST.RESPONSE.redirect(
                self.context.absolute_url() + "?e=%s&msg=%s" % (
                    encodeEmail(sender), mssg))

        else:
            mssg = _(u"You are still subscribed to the mailing list.")
            return REQUEST.RESPONSE.redirect(
                self.context.absolute_url() + "?e=%s&msg=%s" % (
                    encodeEmail(sender), mssg))

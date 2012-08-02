import Acquisition
from DateTime import DateTime

from zope.component import getMultiAdapter
from plone.memoize import instance
from plone.memoize.instance import memoize

from Products.ATContentTypes.interface import IATTopic
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from slc.alertservice import AlertMessageFactory as _

from osha.theme import OSHAMessageFactory as _

class OSHmailSubscribe(BrowserView):
    """View for displaying oshmail 
    """

    def __call__(self, emailaddress, name=''):

        """ helper method to enable osh mail subscription to anonymous user """
        ptool = getToolByName(self.context, 'portal_url')
        portal = ptool.getPortalObject()
        
        pp = getToolByName(portal, 'portal_properties')
        op = getattr(pp, 'osha_properties', None)
        siteadmin = getattr(portal, 'email_from_address')
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
            try:
                msg = unicode(msg, 'iso8859-1').encode('utf-8')
            except:
                pass
            return REQUEST.RESPONSE.redirect(
                referer + "portal_status_message=" + msg)

        if REQUEST.has_key('unsubscribe'):
            return REQUEST.RESPONSE.redirect(self.context.absolute_url() + "/confirm-unsubscription?emailaddress=%s" % (emailaddress))
        else:
            mesg = "subscribe ICT-TEST anonymous\n"
            mssg = "Thank you for subscribing to the OSHmail newsletter. You will receive an email to confirm your subscription."


        #recipient = op.getProperty('listserv_email', siteadmin)
        recipient = 'listserv@list.osha.europa.eu'

        sender = emailaddress
        if name:
            sender = "%s <%s>" % (name, sender)

        subject = ''
        try:
            host.send(mesg, mto=recipient, mfrom=sender, subject=subject)
        except Exception, e:
            mssg = "Your subscription could not be sent. Please try again. " + str(e)

        from slc.alertservice.utils import encodeEmail
        # this feedbackpage has been added to contain a specific tracking code for an external company
        #feedbackpage = "http://osha.europa.eu/news/oshmail/subscription_feedback?portal_status_message=%s&e=%s" % (mssg, encodeEmail(sender))
        return REQUEST.RESPONSE.redirect(refererstem + "?portal_status_message=%s&e=%s" % (mssg, encodeEmail(sender)))

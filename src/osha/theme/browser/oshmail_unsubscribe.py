import Acquisition
from DateTime import DateTime

from zope.component import getMultiAdapter
from plone.memoize import instance
from plone.memoize.instance import memoize

from Products.ATContentTypes.interface import IATTopic
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from slc.alertservice.utils import encodeEmail
from slc.alertservice import AlertMessageFactory as _

from osha.theme import OSHAMessageFactory as _

class OSHmailUnsubscribe(BrowserView):
    """View for displaying oshmail 
    """

    def __call__(self, confirm):

        """ helper method to enable osh mail subscription to anonymous user """
        ptool = getToolByName(self.context, 'portal_url')
        portal = ptool.getPortalObject()
        
        pp = getToolByName(portal, 'portal_properties')
        op = getattr(pp, 'osha_properties', None)
        siteadmin = getattr(portal, 'email_from_address')
        reg_tool = getToolByName(self.context, 'portal_registration')
        host = getToolByName(self.context, 'MailHost')
        REQUEST = self.request
        refererstem = REQUEST.get('HTTP_REFERER').split('?')[0]
        
        #recipient = op.getProperty('listserv_email', siteadmin)
        recipient = 'listserv@list.osha.europa.eu'
        sender = REQUEST.get('confirm_email')

        if confirm =='yes':
            mesg = "unsubscribe ICT-TEST\n"
            mssg = "Thank you! You have been unsubscribed succesfully."
            subject = ''
            try:
                host.send(mesg, mto=recipient, mfrom=sender, subject=subject)
            except Exception, e:
                mssg = "Your unsubscription request could not be sent. Please try again. " + str(e)
            # this feedbackpage has been added to contain a specific tracking code for an external company
            #feedbackpage = "http://osha.europa.eu/news/oshmail/subscription_feedback?portal_status_message=%s&e=%s" % (mssg, encodeEmail(sender))            
            return REQUEST.RESPONSE.redirect(self.context.absolute_url() + "?portal_status_message=%s&e=%s" % (mssg, encodeEmail(sender)))                

        else:
            mssg = "You are still subscribed to the mailing list."
            # this feedbackpage has been added to contain a specific tracking code for an external company
            #feedbackpage = "http://osha.europa.eu/news/oshmail/subscription_feedback?portal_status_message=%s&e=%s" % (mssg, encodeEmail(sender))            
            return REQUEST.RESPONSE.redirect(self.context.absolute_url() + "?portal_status_message=%s&e=%s" % (mssg, encodeEmail(sender)))

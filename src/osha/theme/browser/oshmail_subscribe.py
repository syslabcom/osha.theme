from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from osha.theme import OSHAMessageFactory as _
from quintagroup.captcha.core.utils import (
    decrypt,
    parseKey,
    encrypt1,
)


class OSHmailSubscribe(BrowserView):
    """View for displaying oshmail
    """

    def __call__(self, emailaddress, name=''):

        """ helper method to enable osh mail subscription to anonymous user """

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
            referer += "err=email&msg=%s&" % msg
            return REQUEST.RESPONSE.redirect(referer)

        # validate captcha
        test_key = REQUEST.get('key', '')
        hashkey = REQUEST.get('hashkey', '')
        decrypted_key = decrypt(self.context.captcha_key, hashkey)
        parsed_key = parseKey(decrypted_key)

        index = parsed_key['key']
        date = parsed_key['date']

        if REQUEST.has_key('unsubscribe'):
            return REQUEST.RESPONSE.redirect(
                self.context.absolute_url() +
                "/confirm-unsubscription?emailaddress=%s" % (emailaddress))

        img = getattr(self.context, '%s.jpg' % index)
        solution = img.title
        enc = encrypt1(test_key)
        captcha_tool = getToolByName(self.context, 'portal_captchas')
        if (enc != solution) or (captcha_tool.has_key(decrypted_key)) \
                or (DateTime().timeTime() - float(date) > 3600):
            msg = _(u"Please re-enter validation code.")
            referer += "err=captcha&msg={msg}&emailaddress={emailaddress}&".format(
                msg=msg, emailaddress=emailaddress)
            return REQUEST.RESPONSE.redirect(referer)
        else:
            captcha_tool.addExpiredKey(decrypted_key)

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

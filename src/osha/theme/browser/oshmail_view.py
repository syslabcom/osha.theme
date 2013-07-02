# See #3283

import Acquisition
from DateTime import DateTime

from zope.component import getMultiAdapter
from plone.memoize import instance
from plone.memoize.instance import memoize

from Products.ATContentTypes.interface import IATTopic
from Products.Archetypes.utils import OrderedDict
from Products.CMFCore.utils import getToolByName, isExpired
from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from slc.alertservice import AlertMessageFactory as _

from osha.theme import OSHAMessageFactory as _

class OSHmailView(BrowserView):
    """View for displaying oshmail
    """

    def __call__(self):
        return self.index()

    def getName(self):
        return self.__name__

    @memoize
    def getLatestIssue(self):
        " get the latest published oshmail issue "
        latestissue, issues = self._get_issues()
        return latestissue

    def thisyear(self):
        " return this years number "
        return DateTime().year()

    def lastyear(self):
        " return last years number "
        return DateTime().year() - 1

    def thisyears_issues(self):
        " return this years issues "
        latestissue, issues = self._get_issues()
        return issues.get(self.thisyear(), [])

    def lastyears_issues(self):
        " return last years issues "
        latestissue, issues = self._get_issues()
        return issues.get(self.lastyear(), [])

    def oldernewsletters(self):
        " return all other newsletters older than last years "
        latestissue, issues = self._get_issues()
        if self.thisyear() in issues.keys():
            del issues[self.thisyear()]
        if self.lastyear() in issues.keys():
            del issues[self.lastyear()]
        return issues

    def latest_teasers(self):
        " return the latest teasers from the latest oshmail "
        latest = self.getLatestIssue()
        teasers = []
        try:
            col1 = latest.getObject()['1']['1']
        except KeyError:
            return []
        for aliasid in col1.keys()[1:4]:
            alias = col1[aliasid]
            target = alias.get_target()
            teasers.append(target.Title())
        return teasers

    def get_image(self):
        " find a suitable image to show "
        latest = self.getLatestIssue()
        if latest is None:
            return ''
        try:
            col1 = latest.getObject()['1']['1']
        except KeyError:
            return ''
        for aliasid in col1.keys()[1:4]:
            alias = col1[aliasid]
            target = alias.get_target()
            if hasattr(target.aq_explicit, 'getImage') and target.getImage().get_size() > 0:
                return target.absolute_url() + '/image_thumb'
        return ''


    def get_num_subscribers(self):
        " return the actual number of oshmail subscribers "
        return self.context.portal_properties.osha_properties.getProperty('num_subscribers')

    @memoize
    def _get_issues(self):
        " fetch all oshmail issues "
        folder = self.context.data.oshmail
        pc = self.context.portal_catalog
        yearmap = dict()
        allissues = []
        latestissue = None

        for issue in pc(portal_type='Collage', review_state="published"):
            if not 'oshmail' in issue['getId']:
                continue
            # Don't list OSHMails that are both expired and outdated,
            # aka "deleted"
            if getattr(issue, 'outdated', False) and isExpired(issue):
                continue
            date = issue['effective']
            if latestissue is None or date > latestissue['effective']:
                latestissue = issue
            (name, num) = issue['getId'].split('-')
            yearlist = yearmap.get(date.year(), [])
            yearlist.append((int(num), dict(id=issue['getId'],
                                        day=date.Day(),
                                        month=date.Month(),
                                        year=date.year(),
                                        url=issue.getURL(),
                                        title=issue['Title'])
                                ))

            yearmap[date.year()] = yearlist

        ordered_yearmap = OrderedDict()
        years = yearmap.keys()
        years.sort()
        years.reverse()
        for year in years:
            yearlist = yearmap[year]
            yearlist.sort()
            yearlist.reverse()
            ordered_yearmap[year] = yearlist

        return latestissue, ordered_yearmap
"""
    def subscribe(self, emailaddress, name=''):

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
            mesg = "UNSUBSCRIBE OSHMAIL\n"
            mssg = "Your unsubscription request has been sent."
        else:
            mesg = "SUBSCRIBE OSHMAIL anonymous\n"
            mssg = "Your subscription request has been sent."


        recipient = op.getProperty('listserv_email', siteadmin)

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
"""

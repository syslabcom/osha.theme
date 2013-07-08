""" BrowserViews to replace p4a.calendar listing views: events.html,
past-events.html
"""
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations

from Products.ATContentTypes.interface.folder import IATFolder
from Products.ATContentTypes.interface.topic import IATTopic
from Products.CMFPlone.utils import isExpired


class EventsListingView(BrowserView):
    template = ViewPageTemplateFile('templates/calendar_events_list.pt')
    past_events = False

    def __call__(self):
        return self.template()

    def get_events(self):
        context = self.context
        pc = context.portal_catalog

        if IATTopic.providedBy(context):
            query = context.buildQuery()
        elif IATFolder.providedBy(context):
            current_path = "/".join(context.getPhysicalPath())
            query = {
                "portal_type": "Event",
                "path": { "query": current_path }}
        query["sort_on"] = "start"
        if self.past_events:
            query["start"] = {
                "query": DateTime(), "range" : "max"}
            query["sort_order"] = "reverse"
        else:
            query["start"] = {
                "query": DateTime(), "range" : "min"}
        return pc.searchResults(query)

    def get_event_list(self, start=None, stop=None):
        now = DateTime()
        events = (i.getObject() for i in self.get_events())
        events = (x for x in events if not (
            getattr(x, 'outdated', False) and isExpired(x)))
        months = []
        month_info = []
        old_month_year = None
        for event in events:
            start = event.start()
            month = str(start.month())
            year = str(start.year())
            month_year = year+month
            if month_year != old_month_year:
                old_month_year = month_year
                if month_info:
                    months.append(month_info)
                month_info = {
                    'month': start.month(),
                    'year': start.year(),
                    # e.g. month_oct as used in the plonelocales i18n:domain
                    'month_name': "month_%s" %(
                        start.strftime("%B").lower()[:3] ),
                    'events': []}
            isDateToBeConfirmed = (
                True if hasattr(event, "dateToBeConfirmed")
                and event.dateToBeConfirmed
                else False)
            isOutdated = IAnnotations(event).get("slc.outdated", False)
            event_dict = {'event': event,
                          'day': start.day(),
                          'start': start,
                          'end': event.end(),
                          'location': event.getLocation(),
                          'title': event.Title(),
                          'description': event.Description(),
                          'url': event.absolute_url(),
                          'is_tbc': isDateToBeConfirmed,
                          'is_outdated': isOutdated
                          }
            month_info['events'].append(event_dict)

        if month_info:
            months.append(month_info)
        return months


class PastEventsListingView(EventsListingView):
    past_events = True

""" BrowserViews to replace p4a.calendar listing views: events.html,
past-events.html
"""
from datetime import datetime

from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.ATContentTypes.interface.folder import IATFolder
from Products.ATContentTypes.interface.topic import IATTopic

class EventsListingView(BrowserView):
    template = ViewPageTemplateFile('templates/calendar_events_list.pt')
    past_events = False

    def __call__(self):
        return self.get_events()

    def get_events(self):
        context = self.context
        pc = context.portal_catalog

        if IATTopic.providedBy(context):
            query = context.buildQuery()
        elif IATFolder.providedBy(context):
            current_path = "/" + context.absolute_url(1)
            query = {
                "portal_type": "Event",
                "path": { "query": current_path }}
        if self.past_events:
            query["start"] = {
                "query": DateTime(), "range" : "max"}
        else:
            query["start"] = {
                "query": DateTime(), "range" : "min"}
        return pc.searchResults(query)

    def get_event_list(self, start=None, stop=None):
        now = datetime.datetime.now()
        events = self.get_events()
        months = []
        month_info = []
        old_month_year = None
        for event in events:
            start = event.start
            month = str(start.month)
            year = str(start.year)
            month_year = year+month
            if month_year != old_month_year:
                old_month_year = month_year
                if month_info:
                    months.append(month_info)
                month_info = {'month': start.month,
                              'year': start.year,
                              'month_name': start.strftime("%B"),
                              'events': []}
            event_dict = {'event': event,
                          'day': start.day,
                          'start': start,
                          'end': event.end,
                          'location': event.location,
                          'title': event.title,
                          'description': event.description,
                          'url': event.local_url,
                          }
            month_info['events'].append(event_dict)

        if month_info:
            months.append(month_info)
        return months


class PastEventsListingView(EventsListingView):
    past_events = True

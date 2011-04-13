import datetime

from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base
try:
    from Products.LinguaPlone.interfaces import ITranslatable
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

from p4a.calendar.browser.month import MonthView as p4aMonthView
from p4a.calendar.browser.month import hour_time_formatter

class MonthView(p4aMonthView):
    """View for a month.
    """

    def next_month_link(self):
        year = self.default_day.year
        month = self.default_day.month

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

        return '%s/%s?year=%s&month=%s' % (self.context.absolute_url(),
                                        self.__name__,
                                        year,
                                        month)

    def prev_month_link(self):
        year = self.default_day.year
        month = self.default_day.month

        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1

        return '%s/%s?year=%s&month=%s' % (self.context.absolute_url(),
                                        self.__name__,
                                        year,
                                        month)

    def getIntroductionContent(self):
        """ Look for Document called introduction and return ists BodyText if present.
        """
        if HAS_LINGUAPLONE:
            base = self.context.getCanonical()
        else:
            base = self.context
        if hasattr(aq_base(base), 'introduction'):
            intro = getattr(base, 'introduction', None)
            if HAS_LINGUAPLONE:
                language_tool = getToolByName(self.context, 'portal_languages')
                lang = language_tool.getPreferredLanguage()
                intro = intro.getTranslation(lang) or intro
            if intro:
                return intro.getText()
        return ''

    def _fill_events(self, days, description_length=250, ellipsis='...'):
        """Overriding this method so that the dateToBeConfirmed value
        can be returned in the event_dict"""
        for event in self._events:
            dt = datetime.date(event.start.year,
                               event.start.month,
                               event.start.day)
            dtend = datetime.date(event.end.year,
                                  event.end.month,
                                  event.end.day)

            dt_list = dt in days and [dt] or []
            while dt != dtend:
                dt = dt + datetime.timedelta(1)
                if dt in days:
                    # Don't append the date if it's outside the list of visible days
                    dt_list.append(dt)

            for dt in dt_list:
                day = days.get(dt, None)
                if day is None:
                    # basically the date wasn't in our active month so
                    # we set the date to the first day of the month
                    randomday = days.itervalues().next().daydate
                    newdate = datetime.date(randomday.year, randomday.month, 1)
                    day = days[newdate]

                description = event.description

                if len(description)>description_length:
                    description = description[:description_length]
                    l = description.rfind(' ')
                    if l > description_length/2:
                        description = description[:l+1]
                    description += ellipsis

                timespan = '%s to %s %s' % (hour_time_formatter(self, event.start),
                                            hour_time_formatter(self, event.end),
                                            event.timezone)

                event_dict = {'label': hour_time_formatter(self,event.start) + ' ' + event.title,
                              'timespan': timespan,
                              'local_url': event.local_url,
                              'title': event.title,
                              'location': event.location,
                              'description': description,
                              'type': event.type,
                              'dateToBeConfirmed': event.dateToBeConfirmed}
                day.add(event_dict)

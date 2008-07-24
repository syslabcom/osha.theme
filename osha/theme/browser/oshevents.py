import datetime
from DateTime import DateTime
import calendar
try:
    from Products.Five.browser.pagetemplatefile import \
         ZopeTwoPageTemplateFile as PageTemplateFile
except ImportError:
    from zope.pagetemplate.pagetemplatefile import PageTemplateFile

from zope.component import queryMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from p4a.calendar import interfaces
import Acquisition
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter


class EventListingView(object):
    """View that lists events.
    """
    
    eventlist = PageTemplateFile('templates/oshevents.pt')
    
    def _getEventList(self, start=None, reverse=False):

        context = Acquisition.aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()

        oshaview = getMultiAdapter((self.context, self.request), name=u'oshaview')
        mySEP = oshaview.getCurrentSingleEntryPoint()
        kw = ''
        if mySEP is not None:
            kw = mySEP.getProperty('keyword', '')


        query = dict(portal_type='Event',
                       review_state='published',
                       path=navigation_root_path,
                       sort_on='start'
                       )
        
        if reverse:
            query.update(end={'query': DateTime(),
                              'range': 'max'})
        else:
            query.update(end={'query': DateTime(),
                              'range': 'min'})
                            
        if kw !='':
            query.update(Subject=kw)
        results = catalog(query)


#        provider = interfaces.IEventProvider(self.context)
#        now = datetime.datetime.now()
#        events = list(provider.gather_events(start=start, stop=stop, 
#                                             **self.request.form))
#        import pdb; pdb.set_trace()
#        events.sort()
#        # If this is an archive, revert the event list.
#        if reverse:
#            events.reverse()
        months = []
        month_info = []
        old_month_year = None
        for event in results:
            start = event.start
            month = str(start.month())
            year = str(start.year())
            month_year = year+month
            if month_year != old_month_year:
                old_month_year = month_year
                if month_info:
                    months.append(month_info)
                month_info = {'month': month,
                              'year': year,
                              'month_name': start.strftime("%B"),
                              'events': []}
            event_dict = {'event': event,
                          'day': start.day,
                          'start': start,
                          'end': event.end,
                          'location': event.location,
                          'title': event.Title,
                          'description': event.description,
                          'url': event.getURL(),
                          }
            month_info['events'].append(event_dict)

        if month_info:
            months.append(month_info)
            
        return months
        
    def upcomingEvents(self):
        now = datetime.datetime.now()
        months = self._getEventList(start=now)
        return self.eventlist(months=months, show_past=False)

    def pastEvents(self):
        now = datetime.datetime.now()
        months = self._getEventList(start=now, reverse=True)
        return self.eventlist(months=months, show_past=True)

    def event_creation_link(self, start=None, stop=None):
        provider = interfaces.IEventProvider(self.context)
        return provider.event_creation_link(start, stop)

    def render_filter(self):
        provider = queryMultiAdapter(
            (self.context, self.request, self), 
            IContentProvider, 'eventfilter')
        if provider is None:
            return ''
        provider.update()
        return provider.render()
 
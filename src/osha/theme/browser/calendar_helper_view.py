"""
Helper view and method for adding functionality to customised
p4a.calendar code
"""


def getEventDateToBeConfirmed(event):
    return hasattr(event, "dateToBeConfirmed") and event.dateToBeConfirmed


class CalendarHelperView(object):
    """ A helper view to provide extra methods to customised
    p4a.calendar code
    """

    def getDateToBeConfirmed(self, brain_event):
        "get the schemaextended dateToBeConfirmed"
        if brain_event.has_key("event"):
            event = brain_event["event"]._getEvent()
        elif hasattr(brain_event, "getObject"):
            event = brain_event.getObject()
        return getEventDateToBeConfirmed(event)

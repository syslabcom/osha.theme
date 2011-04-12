"""
Helper view and method for adding functionality to customised
p4a.calendar code
"""


def getEventDateToBeConfirmed(event):
    if event.Schema().has_key("dateToBeConfirmed") \
            and event.dateToBeConfirmed:
        return True
    else:
        return False


class CalendarHelperView(object):
    """ A helper view to provide extra methods to customised
    p4a.calendar code
    """

    def getDateToBeConfirmed(self, brain_event):
        "get the schemaextended dateToBeConfirmed"
        event = brain_event["event"]._getEvent()
        return getEventDateToBeConfirmed(event)

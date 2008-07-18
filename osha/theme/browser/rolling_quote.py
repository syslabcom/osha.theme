import random
from zope import schema
from osha.theme.interfaces import IRolling_quotes
from plone.app.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

class IRollingQuotes(IPortletDataProvider):
"""at the moment there is nothing to configure"""

class Assignment(base.Assignment):
    def __init__(self):
        """nothing to initialize here"""

    @property
    def quote(self) :
        return _(u"Quotation")



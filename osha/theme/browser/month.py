from p4a.calendar.browser.month import MonthView as p4aMonthView
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base
try:
    from Products.LinguaPlone.interfaces import ITranslatable
except ImportError:
    HAS_LINGUAPLONE = False
else:
    HAS_LINGUAPLONE = True

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

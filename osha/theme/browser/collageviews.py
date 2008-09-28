from Products.Collage.browser.views import BaseView

class TeaserView(BaseView):
    title = u'Teaser'

class DocumentHeadlineView(BaseView):
    title = u'Headline'

class DocumentRightcolHealineView(BaseView):
    title = u'Headline (right column)'

class OSHLinkFullView(BaseView):
    title = u'Full'

class NewsRightColumnView(BaseView):
    title = u'Simple (right column)'

class EventRightColumn(BaseView):
    title = u'Simple (right column)'

class PublicationView(BaseView):
    title = u'Publication'

class PressReleaseBaseView(BaseView):
    title = 'Headline'

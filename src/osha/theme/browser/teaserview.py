from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner, aq_parent, aq_base
from zope.component import getMultiAdapter
from DateTime import DateTime


class TeaserView(BrowserView):
    """ used for displaying teasers"""
    
    template = ViewPageTemplateFile('templates/teaser_view.pt')
    template.id = "teaser-view"

    def __call__(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_languages = getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()

        # try to get query parameters from Topic (if present)
        query = getattr(context, 'buildQuery', None) and context.buildQuery()

        if not query:
            # search in the navigation root of the currently selected language and in the English path
            # with Language = preferredLanguage or neutral
            paths = list()
            portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
            navigation_root_path = portal_state.navigation_root_path()
            navigation_root = portal_state.portal().restrictedTraverse(navigation_root_path)
            teaser = getattr(navigation_root, 'teaser', None)
            if teaser:
                teaser_path = '/'.join(teaser.getPhysicalPath())
                paths.append(teaser_path)
                try:
                    canonical_path = '/'.join(teaser.getCanonical().getPhysicalPath())
                    paths.append(canonical_path)
                except:
                    pass

            state = 'published'
            now = DateTime()
            query = dict(portal_type='News Item',
                           review_state=state,
                           path=paths,
                           effective={'query': now,
                                'range': 'max'},
                           expires={'query': now,
                                'range': 'min'},
                           sort_on='effective',
                           sort_order='reverse',
                           Language=['', preflang])

        self.items = catalog(query)
        return self.template()


    def getBodyText(self):
        """ returns body text of collection if present """
        context = aq_base(aq_inner(self.context))
        text = getattr(context, 'getText', None) and context.getText() or ''
        return text
    
    def showLinkToNewsItem(self):
        return self.context.getProperty('show_link_to_news_item', True)


class TeaserArchiveView(TeaserView):
    """ used for displaying archived  teasers"""
    
    template = ViewPageTemplateFile('templates/teaser_view.pt')
    template.id = "teaser-archive-view"

    def __call__(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')
        portal_languages = getToolByName(self.context, 'portal_languages')
        preflang = portal_languages.getPreferredLanguage()


        # search in the navigation root of the currently selected language and in the English path
        # with Language = preferredLanguage or neutral
        paths = list()
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        navigation_root = portal_state.portal().restrictedTraverse(navigation_root_path)
        teaser = getattr(navigation_root, 'teaser', None)
        if teaser:
            teaser_path = '/'.join(teaser.getPhysicalPath())
            paths.append(teaser_path)
            try:
                canonical_path = '/'.join(teaser.getCanonical().getPhysicalPath())
                paths.append(canonical_path)
            except:
                pass

        state = 'published'
        now = DateTime()
        query = dict(portal_type='News Item',
                       review_state=state,
                       path=paths,
                       effective={'query': now,
                            'range': 'max'},
                       expires={'query': now,
                            'range': 'max'},
                       sort_on='effective',
                       sort_order='reverse',
                       Language=['', preflang])
                       
        self.items = catalog(query)
        return self.template()


from Products.Collage.browser.views import BaseView as CollageBaseView
from AccessControl import getSecurityManager, Unauthorized
from zope.interface import directlyProvidedBy, directlyProvides
from zope.component import getMultiAdapter
import Acquisition
from Products.Collage.interfaces import ICollageBrowserLayer, IDynamicViewManager
from Products.Collage.interfaces import ICollageAlias, ICollage, ICollageRow, ICollageColumn
from Products.Collage.utilities import isTranslatable
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

class BaseView(CollageBaseView):

    def getCollageContext(self):
        return self._collage_context

    def getCollageId(self):
        return self._collage_context is not None and self._collage_context.getId() or ''
        

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

class DocumentTextView(BaseView):
    title = 'Text'

class SimpleContainerRenderer(BrowserView):
    def getItems(self, contents=None):
        # needed to circumvent bug :-(
        self.request.debug = False

        # transmute request interfaces
        ifaces = directlyProvidedBy(self.request)
        directlyProvides(self.request, ICollageBrowserLayer)

        views = []

        if not contents:
            contents = self.context.folderlistingFolderContents()

        # make sure the languager passed in via set_language is applied correctly
        plt = getToolByName(self.context, 'portal_languages')
        binding = self.request.get('LANGUAGE_TOOL', None)
        language = self.request.get('set_language', plt.getPreferredLanguage())
        if binding and binding.LANGUAGE != language:
            binding.LANGUAGE = language

        for context in contents:
            target = context
            manager = IDynamicViewManager(context)
            layout = manager.getLayout()

            if not layout:
                layout, title = manager.getDefaultLayout()

            if ICollageAlias.providedBy(context):
                target = context.get_target()

                # if not set, revert to context
                if target is None:
                    target = context

                # verify that target is accessible
                try:
                    getSecurityManager().validate(self, self, target.getId(), target)
                except Unauthorized:
                    continue

            # Filter out translation duplicates:
            # If a non-alias object is translatable, check if its language
            # is set to the currently selected language or to neutral,
            # or if it is the canonical version
            elif isTranslatable(target):
                language = self.request.get('LANGUAGE','')
                if target.Language() not in (language, ''):
                    # Discard the object, if it is not the canonical version
                    # or a translation is available in the requested language.
                    if not target.isCanonical() or target.getTranslation(language) in contents:
                        continue
                # If the target is a translation, get the layout defined on the canonical
                # object, unless a layout has already been defined on the translation.
                # Fallback to default layout.
                if not target.isCanonical():
                    canmanager = IDynamicViewManager(target.getCanonical())
                    layout = manager.getLayout() or canmanager.getLayout() or layout

            # assume that a layout is always available
            view = getMultiAdapter((target, self.request), name=layout)

            # store reference to alias if applicable
            if ICollageAlias.providedBy(context):
                view.__alias__ = context


            view._collage_context = self.getCollageContext(self.context)
            views.append(view)

        # restore interfaces
        directlyProvides(self.request, ifaces)

        return views

    def getCollageContext(self, context):
       # import pdb; pdb.set_trace()
        if ICollageRow.providedBy(context) or ICollageColumn.providedBy(context):
            return self.getCollageContext(context.aq_parent)
        if ICollage.providedBy(context):
            return context
        else:
            return self.context

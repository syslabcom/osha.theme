class HelperView(object):
    """Helper view to make generally useful methods available to all
    page templates.

    To call a method:
    <tal:block define="helper_view context/@@helper-view">
      <p tal:content="python:helper_view.get_sorted([3,2])"></p>
    </tal:block>

    Note: new methods must be added to the zcml allowed_attributes
    (otherwise it is not allowed to access them from other views)
    """

    def get_sorted(self, collection, key=None, reverse=False):
        """Allows sorted() to be used from any page template"""
        return sorted(collection, key=key, reverse=reverse)

    def get_native_language_by_code(self, lang_code):
        context = self.context
        ltool = context.portal_languages
        lang_info = ltool.getAvailableLanguageInformation().get(lang_code, None)
        if lang_info is not None:
            return lang_info.get(u"native", None)
        return None

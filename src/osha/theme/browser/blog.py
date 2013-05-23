from Products.Five.browser import BrowserView
from plone import api


class BlogView(BrowserView):
    """View for the front page of the Blog section."""

    def __call__(self):
        return self.index()

    def blog_items(self):
        """Return blog items from the blog folder"""
        return self._get_blog_items(folder=self.context.aq_parent)

    def _get_blog_items(self, folder=None):
        """Return a list of blog items. If blog entry is not available in
        currently selected language, use the canonical version ('en').

        :param folder: folder where to get the blog items from
        :returns: a list of 'Blog Entry' objects
        """
        if not folder:
            return
        catalog = api.portal.get_tool('portal_catalog')
        path_en = '/'.join(folder.getCanonical().getPhysicalPath())
        items_en = catalog(
            portal_type=['Blog Entry'],
            Language='all',
            path={"query": path_en},
            sort_on='effective',
            sort_order='descending'
        )

        results = []
        for item in items_en:
            obj = item.getObject()
            obj_translation = obj.getTranslation()

            if obj_translation:
                results.append(obj_translation)
            else:
                results.append(obj)

        return results


class DirectorCornerView(BlogView):
    """View for the front page of Director's Corner."""

    def __call__(self):
        return self.index()

    def blog_items(self):
        """Return blog items from the blog subfolder"""
        blog_folder = self.context.aq_parent.get('blog')
        if blog_folder:
            return self._get_blog_items(folder=blog_folder)

    def blog_intro(self):
        """Return the blog introductory text."""
        try:
            blog_page = self.context.aq_parent['blog']['front-page']
            return blog_page.getText()
        except (AttributeError, KeyError):
            return


class BlogRssView(BlogView):
    """RSS view for the blog folder"""

    def __call__(self):
        return self.index()

    def blog_items(self):
        """Return blog items from this folder."""
        return self._get_blog_items(folder=self.context)

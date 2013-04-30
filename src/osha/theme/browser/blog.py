from Products.Five.browser import BrowserView
from plone import api

BLOG_PATH = '/en/blog'


class BlogView(BrowserView):
    """View that displays a list of blog entries."""

    def __call__(self):
        return self.index()

    def blog_description(self):
        """Return the blog description"""
        portal = api.portal.get()
        try:
            blog_path = "/".join(portal.getPhysicalPath()) + BLOG_PATH
            blog = portal.restrictedTraverse(blog_path)
            return blog.getDescription()
        except (AttributeError, KeyError):
            # blog not found
            return

    def blog_items(self):
        """Return a list of blog items. If blog entry is not available in
        currently selected language, use the canonical version ('en').

        :returns: a list of 'Blog Entry' objects
        """
        portal = api.portal.get()
        path_en = "/".join(portal.getPhysicalPath()) + BLOG_PATH
        catalog = api.portal.get_tool('portal_catalog')
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

    def blog_intro(self):
        """Return introductory text which we fetch from a page in the folder
        with id 'blog-intro'. If page is not available in currently selected
        language, use the canonical version ('en').
        """
        page = self.context.get('blog-intro') or \
               self.context.getCanonical().get('blog-intro')

        try:
            text = page and page.getText() or None
        except AttributeError:
            # object found but doesn't have a text field (wrong type)
            text = None
        return text

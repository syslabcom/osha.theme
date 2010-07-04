import logging

from Acquisition import aq_base, aq_inner, aq_acquire

from Products.Five.browser import BrowserView
from zope.publisher.interfaces import NotFound
from zope.component import getMultiAdapter

logger = logging.getLogger('osha.theme/browser/telescope.py')

class TelescopeView(BrowserView):
    """
    Renders an object in a different location of the site when passed the
    path to it #1150
    """

    def __call__(self, *args, **kw):
        """
        Uses ac_aqcuire to return the specified page template
        """
        if self.request.has_key("path"):
            path = self.request["path"]
            target_obj = None
            try:
                target_obj = self.context.restrictedTraverse(path)
            except KeyError:
                logger.log(logging.INFO, "Invalid path: %s" %path)
                raise NotFound
            if target_obj:
                context = self.context
                request = self.request
                view = ""
                try:
                    # Strip the target_obj of context with aq_base.
                    # Put the target in the context of self.context.
                    # getDefaultLayout returns the name of the default
                    # view method from the factory type information
                    view = aq_acquire(aq_base(target_obj).__of__(context),
                                       target_obj.getDefaultLayout())(**kw)

                except AttributeError, message:
                    logger.log(logging.ERROR,
                               "Error acquiring template: %s, path: %s"\
                               %(message, path))
                    raise NotFound
                if view:
                    # All images and links in the target document
                    # which depend on the context e.g. images in News
                    # items, will be broken, so we do a simple replace
                    # to fix them.

                    # I tried to be a bit more clever about this and
                    # use the lxml soupparser, but it breaks the
                    # layout severely when it is converted back to
                    # html (deroiste)
                    proxy_url = context.absolute_url() + "/" +\
                                 target_obj.getId()
                    target_url = target_obj.absolute_url()
                    return view.replace(proxy_url, target_url)

        else:
            logger.log(logging.INFO, "No path specified")
            raise NotFound

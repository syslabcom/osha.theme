import logging
from Acquisition import aq_base, aq_inner, aq_acquire
from Products.Five.browser import BrowserView
from zope.publisher.interfaces import NotFound

logger = logging.getLogger('osha.theme/browser/telescope.py')

class TelescopeView(BrowserView):
    """
    Renders an object in a different location of the site when passed the
    path to it #1150
    """
    def __call__(self, *args, **kw):
        """
        Uses aq_aqcuire to return the specified page template
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
                try:
                    # Strip the target_obj of context with aq_base.
                    # Put the target in the context of self.context.
                    # getDefaultLayout returns the name of the default
                    # view method from the factory type information
                    return aq_acquire(aq_base(target_obj).__of__(self.context),
                                      target_obj.getDefaultLayout())(**kw)
                except AttributeError, message:
                    logger.log(logging.ERROR,
                               "Error acquiring template: %s, path: %s"\
                               %(message, path))
                    raise NotFound
        else:
            logger.log(logging.INFO, "No path specified")
            raise NotFound

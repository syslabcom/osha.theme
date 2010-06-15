import logging
from Acquisition import aq_inner, aq_acquire
from Products.Five.browser import BrowserView

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
        default_error_message = aq_acquire(self.context,
                                           "default_error_message")
        if self.request.has_key("path"):
            path = self.request["path"]
            target_obj = None
            try:
                target_obj = aq_inner(self.context.restrictedTraverse(path))
            except KeyError:
                logger.log(logging.INFO, "Invalid path: %s" %path)
                return default_error_message()
            if target_obj:
                try:
                    # getDefaultLayout returns the name of the default
                    # view method from the factory type information
                    return aq_acquire(target_obj,
                                      target_obj.getDefaultLayout())(**kw)
                except AttributeError, message:
                    logger.log(logging.ERROR,
                               "Error acquiring template: %s, path: %s"\
                               %(message, path))
                    return default_error_message()
        else:
            logger.log(logging.INFO, "No path specified")
            return default_error_message()

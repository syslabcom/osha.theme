from plone.app.layout.globals.layout import LayoutPolicy
from osha.theme.browser.interfaces import IFullWidth
from slc.subsite.root import getSubsiteRoot


class OSHALayoutPolicy(LayoutPolicy):
    """A view that gives access to various layout related functions.
    """

    def bodyClass(self, template, view):
        """Return the CSS class to be used on the body tag,
        with additional classes as required by the OSHA theme"""
        body_class = super(OSHALayoutPolicy, self).bodyClass(template, view)
        if IFullWidth.providedBy(self.context):
            body_class = u"%s full-width" % body_class
        subsite_path = getSubsiteRoot(self.context)
        body_class = u"%s subsite-%s" % (body_class, \
            subsite_path.split('/')[-1])

        return body_class

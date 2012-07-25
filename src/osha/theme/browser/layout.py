from plone.app.layout.globals.layout import LayoutPolicy
from osha.theme.browser.interfaces import IFullWidth
from zope.component import getMultiAdapter
from slc.subsite.root import getSubsiteRoot

class OSHALayoutPolicy(LayoutPolicy):
    """A view that gives access to various layout related functions.
    """

    def bodyClass(self, template, view):
        """Return the CSS class to be used on the body tag,
        with additional classes as required by the OSHA theme"""
        context = self.context
        portal_state = getMultiAdapter(
            (context, self.request), name=u'plone_portal_state')
        navroot = portal_state.navigation_root()
        
        body_class = super(OSHALayoutPolicy, self).bodyClass(template, view)
        if IFullWidth.providedBy(self.context):
            body_class = u"%s full-width" % body_class

        contentPath = context.getPhysicalPath()[len(navroot.getPhysicalPath()):]
        if contentPath:
            for i in range(len(contentPath)):
                body_class += " subsection%s-%s" % (i, contentPath[i])

        subsite_path = getSubsiteRoot(self.context)
        body_class = u"%s subsite-%s" % (body_class, \
            subsite_path.split('/')[-1])

        return body_class

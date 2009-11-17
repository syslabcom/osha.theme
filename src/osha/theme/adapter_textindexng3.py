from Products.TextIndexNG3.adapters.cmf_adapters import CMFContentAdapter
from Products.ATContentTypes.interface.file import IATFile
from Products.PluginIndexes.common import safe_callable
from Products.CMFCore.interfaces import IContentish
from zope.component import adapts


class ContentAdapter(CMFContentAdapter):
    """ An adapter for CMF content.
        addSearchableTextField is overwritten to make sure we don't try to call a string
    """
    adapts(IContentish)

    def addSearchableTextField(self, icc):
        st = self.context.SearchableText
        if safe_callable(st):
            st = st()
        text = self._c(st)
        icc.addContent('SearchableText', text, self.language)


class ATFileAdapter(CMFContentAdapter):

    """An adapter for ATCT files.
    """

    adapts(IATFile)

    def addSearchableTextField(self, icc):
        st = self.context.SearchableText
        if safe_callable(st):
            st = st()
        text = self._c(st)
        icc.addContent('SearchableText', text, self.language)

        f = self.context.getFile()
        if not f:
            return

        body = str(f)
        if body:
            mt = f.getContentType()
            if mt == 'text/plain':
                icc.addContent('SearchableText', self._c(body), self.language)
            else:
                icc.addBinary('SearchableText', body, mt, None, self.language)

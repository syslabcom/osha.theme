import unittest
import doctest

from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from osha.theme.browser import oshnetwork_member_view
from osha.theme.tests.base import OshaThemeTestCase
from osha.theme.portlets import network_member_links

class TestView(OshaThemeTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def populateSite(self):
        """ Populate the test site with some content. """

        self.portal.invokeFactory("Folder", "en")
        self.portal.en.invokeFactory("Folder", "belgium")
        self.portal.en.belgium.invokeFactory("Document", "index_html")
        ltool = self.portal.portal_languages
        ltool.addSupportedLanguage('nl')

    def test_view_methods(self):
        """ Test the methods in the oshnetwork-member-view class """
        self.populateSite()

        view = self.portal.en.belgium.index_html.restrictedTraverse("@@oshnetwork-member-view")
        localized_path = view.getLocalizedPath("asdf")
        self.assertEquals(localized_path,
                          "/en/asdf")

        # Change the language
        view.context.setLanguage("nl")
        localized_path = view.getLocalizedPath("asdf")
        self.assertEquals(localized_path,
                          "/nl/asdf")

class TestPortlet(OshaThemeTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='osha.NetworkMemberLinks')
        self.assertEquals(portlet.addview,
            'osha.NetworkMemberLinks')

    def test_interfaces(self):
        portlet = network_member_links.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='osha.NetworkMemberLinks')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   network_member_links.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = network_member_links.Assignment()
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, network_member_links.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        assignment = network_member_links.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, network_member_links.Renderer))


class TestRenderer(OshaThemeTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        assignment = assignment or network_member_links.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def populateSite(self):
        """ Populate the test site with some content. """

        self.portal.invokeFactory("Folder", "en")
        self.portal.en.invokeFactory("Folder", "belgium")
        self.portal.en.belgium.invokeFactory("Document", "index_html")
        ltool = self.portal.portal_languages
        ltool.addSupportedLanguage('nl')

    def test_render(self):
        self.populateSite()

        # Test the rendered portlet
        render_portlet = self.renderer(context=self.portal.en.belgium.index_html,
                          assignment=network_member_links.Assignment())
        render_portlet = render_portlet.__of__(self.folder)
        render_portlet.update()

        # TODO: actually test it :)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestView))
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite

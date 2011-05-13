import logging
from zope import component

from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from osha.theme.portlets import osha_items
from osha.theme.tests.base import OshaThemeTestCase

log = logging.getLogger('test_osha_items_portlet.py')

class TestPortlet(OshaThemeTestCase):

    def afterSetUp(self):
        self.loginAsPortalOwner()

    def test_portlet_registered(self):
        portlet = component.getUtility(IPortletType, name="osha.OSHAItems")
        self.assertEquals(portlet.addview, "osha.OSHAItems")

    def test_portlet_interfaces(self):
        portlet = osha_items.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_addview(self):
        portlet = component.getUtility(IPortletType, name='osha.OSHAItems')
        mapping = self.portal.restrictedTraverse('++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={
                                'count':5, 
                                'state':('published', ), 
                                'subject':('category1', 'category2'), 
                                'header':'Testing OSHA Items Portlet',
                                })
        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0], osha_items.Assignment))
        assignment = mapping.values()[0]
        self.assertEquals(assignment.count, 5)
        self.assertEquals(assignment.state, ('published',))
        self.assertEquals(assignment.subject, ('category1', 'category2'))
        self.assertEquals(assignment.header, 'Testing OSHA Items Portlet')

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = osha_items.Assignment()
        editview = component.getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, osha_items.EditForm))

    def test_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')

        manager = component.getUtility(
                                IPortletManager, 
                                name='plone.rightcolumn', 
                                context=self.portal
                                )

        assignment = osha_items.Assignment()

        renderer = component.getMultiAdapter(
                                (context, request, view, manager, assignment), 
                                IPortletRenderer
                                )

        self.failUnless(isinstance(renderer, osha_items.Renderer))


class TestRenderer(OshaThemeTestCase):
    
    def afterSetUp(self):
        """ Create a object, and call the relevant event to enable the
            auto-creation of the sub-objects ('speakers', 'speech venues').
        """
        self.loginAsPortalOwner()

    def renderer(self, context=None, request=None, view=None, manager=None, assignment=None):
        """ """
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or component.getUtility(IPortletManager, 
                                        name='plone.rightcolumn', 
                                        context=self.portal)
        assignment = assignment or osha_items.Assignment()
        return component.getMultiAdapter(
                                (context, request, view, manager, assignment), 
                                IPortletRenderer)

    # def test_portlet(self):
    #     """ """
    #     total_seminars = 10
    #     seminars = self.portal.objectValues('SPSeminar')
    #     seminars_urls = ['/'.join(s.getPhysicalPath()) for s in seminars]

    #     assignment = osha_items.Assignment(**{
    #                                 'count':5, 
    #                                 'state':('published', ), 
    #                                 'header':'Testing Seminars Portlet',
    #                                 })

    #     r = self.renderer(
    #                 context=self.portal, 
    #                 assignment=assignment,
    #                 )

    #     # Test that no seminars exist yet and that the portlet will not be
    #     # available because of it.
    #     seminars = r._data()
    #     self.assertEquals(len(seminars), 0)
    #     self.assertEquals(r.available, False)

    #     # Create test data.
    #     create_test_seminars(self.portal, total_seminars, False, False)

    #     # Test that the portlet returns the correct amount of seminars
    #     seminars = r._data()
    #     self.assertEquals(len(seminars), 5)

    #     # Test that it's actually Seminars being returned.
    #     for seminar in seminars:
    #         self.assertEquals(seminar.portal_type, 'SPSeminar')

    #     # Test with diffferent count values:
    #     for count in range(0, 12):
    #         assignment = osha_items.Assignment(**{
    #                                         'count': count, 
    #                                         'state':('published', ), 
    #                                         'subject':(), 
    #                                         'header':'Testing Seminars Portlet',
    #                                         })
    #         r = self.renderer(
    #                     context=self.portal, 
    #                     assignment=assignment,
    #                     )
    #         seminars = r._data()
    #         self.assertEquals(len(seminars), count > total_seminars and total_seminars or count)

    #         if count == 0:
    #             self.assertEquals(r.available, False)
    #         else:
    #             self.assertEquals(r.available, True)

    #     # Test that subject filtering works:
    #     for cat in ['cat1', 'cat2', 'cat3',]:
    #         assignment = osha_items.Assignment(**{
    #                                         'count':count, 
    #                                         'state':('published', ), 
    #                                         'subject':(cat,), 
    #                                         'header':'Testing Seminars Portlet',
    #                                         })
    #         r = self.renderer(
    #                     context=self.portal, 
    #                     assignment=assignment,
    #                     )
    #         seminars = r._data()
    #         for seminar in seminars:
    #             self.assertEquals(seminar.Subject, (cat,))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    # suite.addTest(makeSuite(TestRenderer))
    return suite

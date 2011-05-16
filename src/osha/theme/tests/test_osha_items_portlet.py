import logging
import random
from zope import component
from zope import event

from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletRenderer

from plone.app.portlets.storage import PortletAssignmentMapping

from Products.Archetypes.event import ObjectInitializedEvent
from Products.CMFCore.utils import getToolByName

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

    def create_test_objects(self, type_name, subject='random', start=0, total=10, publish=True):
        objs = []
        object_ids = \
            ['%s-%s' % (type_name, number) for number in range(start, total+start)]
        parent = self.portal
        for object_id  in object_ids:
            parent.invokeFactory(type_name, 
                                object_id, 
                                title="Title for %s" % type_name, 
                                description="Description for %s" % type_name, 
                                )
            obj = getattr(parent, object_id)
            obj._renameAfterCreation(check_auto_id=True)
            if subject == 'random':
                obj.setSubject(random.sample(['cat1', 'cat2', 'cat3'], 1)[0])
            else:
                obj.setSubject(subject)
            obj.reindexObject()
            event.notify(ObjectInitializedEvent(obj))
            if publish:
                wftool = getToolByName(self.portal, 'portal_workflow')
                wftool.doActionFor(obj, 'publish')
            objs.append(obj)
        return objs
        

    def test_portal_types(self):
        """ Test that only objects of a certain types is returned"""

        for portal_type in ['PressRelease', 'Folder', 'Document']:
            assignment = osha_items.Assignment(**{
                                        'count':5, 
                                        'header':'Testing PressReleases Portlet',
                                        'portletlink':None,
                                        'sort':'effective',
                                        'state':('published',), 
                                        'subject':tuple(), 
                                        'types': (portal_type),
                                        })

            r = self.renderer(
                        context=self.portal, 
                        assignment=assignment,
                        )

            # Create test data.
            total_objects = 5
            self.create_test_objects(portal_type, total=total_objects)

            # Test that the portlet returns the correct amount of objects
            objects = r._data()
            self.assertEquals(len(objects), 5)

            # Test that it's actually objects being returned.
            for seminar in objects:
                self.assertEquals(seminar.portal_type, portal_type)



    def test_count(self):
        """ Test with diffferent count values """
        total_objects = 10
        self.create_test_objects("PressRelease", total=total_objects)
        for count in range(0, 12):
            assignment = osha_items.Assignment(**{
                                            'count':count, 
                                            'header':'Testing PressReleases Portlet',
                                            'portletlink':None,
                                            'sort':'effective',
                                            'state':('published',), 
                                            'subject':tuple(), 
                                            'types': ('PressRelease'),
                                            })
            r = self.renderer(
                        context=self.portal, 
                        assignment=assignment,
                        )
            objects = r._data()
            self.assertEquals(len(objects), count > total_objects and total_objects or count)

            if count == 0:
                self.assertEquals(r.available, False)
            else:
                self.assertEquals(r.available, True)


    def test_categories(self):
        """ """
        total_objects = 5
        # test that subject filtering works:
        i = 0
        for cat in ['cat1', 'cat2', 'cat3',]:
            self.create_test_objects("PressRelease", subject=cat, start=i*total_objects, total=total_objects)
            i += 1
            assignment = osha_items.Assignment(**{
                                        'count':total_objects, 
                                        'state':('published', ), 
                                        'subject':(cat,), 
                                        'header':'Testing objects portlet',
                                        'types': ('PressRelease'),
                                        })
            r = self.renderer(
                        context=self.portal, 
                        assignment=assignment,
                        )
            objects = r._data()
            self.assertEquals(len(objects), total_objects)
            for ob in objects:
                self.assertEquals(ob.Subject, (cat,))


    def test_sorting_criteria(self):
        """ """
        total_objects = 5
        self.create_test_objects("PressRelease", total=total_objects)
        assignment = osha_items.Assignment(**{
                                        'count':5, 
                                        'header':'Testing PressReleases portlet',
                                        'portletlink':None,
                                        'sort':'sortable_title',
                                        'state':('published',), 
                                        'subject':tuple(), 
                                        'types': ('PressRelease'),
                                        })

        r = self.renderer(
                    context=self.portal, 
                    assignment=assignment,
                    )
        objects = r._data()
        self.assertEquals(len(objects), total_objects)

        titles = [seminar.Title for seminar in objects]
        sorted_titles = titles
        sorted_titles.sort()
        self.assertEquals(titles, sorted_titles)



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite

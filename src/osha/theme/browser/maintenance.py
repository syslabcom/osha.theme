# -*- coding: utf-8 -*-
"""Do some maintenance on the migrated site."""
from Acquisition import aq_base
import transaction
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.interface import implements

from osha.theme.browser.interfaces import IMaintenanceView
from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.content.folder import ATFolder


def convertLPFolder(parent, folder):
    """ convert Large Plone Folders to Folders """
    id = folder.getId()
    newfolder = ATFolder(id)
    newfolder._setId(id)
    newfolder = newfolder.__of__(parent)

    uid = folder._at_uid

    for item_id, item in folder.objectItems():
        folder._objects = tuple(
            [i for i in folder._objects if i['id'] != item_id])
        folder._delOb(item_id)

        newfolder._objects = newfolder._objects + (
            {'id': item_id, 'meta_type': item.meta_type},)
        newfolder._setOb(item_id, aq_base(item))

    parent._objects = tuple([i for i in parent._objects if i['id'] != id])
    parent._delOb(id)

    newfolder._at_uid = uid
    parent._objects = parent._objects + (
        {'id': id, 'meta_type': newfolder.meta_type},)
    parent._setOb(id, aq_base(newfolder))

    #transaction.abort()
    return "converted %s" % id

def findLPFolder(context):
    for id, item in context.ZopeFind(context, search_sub=0):
        if item.meta_type == 'ATBTreeFolder':
            print convertLPFolder(context, item)
        if item.isPrincipiaFolderish:
            findLPFolder(item)

class MaintenanceView(BrowserView):
    """ the view to run the import steps """

    implements(IMaintenanceView)

    def __call__(self):
        return 42

    def convertLPFolders(self):
        """ find and convert all LP Folders """
        print "starting conversion"
        findLPFolder(self.context)
        print "conversion done"

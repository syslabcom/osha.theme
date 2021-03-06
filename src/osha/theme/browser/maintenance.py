# -*- coding: utf-8 -*-
"""Do some maintenance on the migrated site."""
from Acquisition import aq_base
import transaction
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implements
from plone.app.async.interfaces import IAsyncService

from osha.theme.browser.interfaces import IMaintenanceView
from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes.content.folder import ATFolder
import logging
log = logging.getLogger('osha.theme/maintenance.py')

log_file = open("converted_large_plone_folders.log", "a")


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
    return "%s, %s" % (id, folder.absolute_url(1))

def findLPFolder(context):
    for id, item in context.ZopeFind(context, search_sub=0):
        if item.meta_type == 'ATBTreeFolder':
            msg = convertLPFolder(context, item)
            print msg
            log_file.write(msg + "\n")
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


class QueueSize(BrowserView):
    """ Return the length of the default queue """

    def __call__(self):
        async = getUtility(IAsyncService)
        queues = async.getQueues()
        queue = queues.get('', None)
        if queue is None:
            return "No default queue found"
        return "The default queue has %d items" % len(queue)


class RemoveFromQueue(BrowserView):
    """ remove the first x items from the queue """

    def __call__(self):
        async = getUtility(IAsyncService)
        queues = async.getQueues()
        queue = queues.get('', None)
        if queue is None:
            return "No default queue found"
        amount = self.request.get('amount', 1)
        try:
            amount = int(amount)
        except:
            amount = 1
        cnt = 0
        for item in queue:
            if cnt < amount:
                path = "/".join(item.args[0])
                log.info('Remove item with path %s' % path)
                queue.remove(item)
                cnt += 1
            else:
                break
        res = "I removed %d items from the queue, it now has %d items" % (cnt,
            len(queue))
        log.info(res)
        return res

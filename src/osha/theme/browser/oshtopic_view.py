import Acquisition, urllib2
from types import *
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from osha.theme import OSHAMessageFactory as _
from zope.i18n import translate

class OSHTopicView(BrowserView):
    """View for displaying the results of a topic outside the current context within the context
    """
    template = ViewPageTemplateFile('templates/oshtopic_view.pt')
    template.id = 'oshtopic-view'
    
    
    def __call__(self):
        topicpath = self.request.get('tp', None)
        if topicpath is None:
            return urllib2.HTTPError(self.request.URL, 
                                    '400', 'Bad Request', 
                                    {}, fp=None)
        if topicpath.startswith('/') and not topicpath.startswith('/osha/portal'):
            topicpath = topicpath[1:]
        self.tp = topicpath
        return self.template() 
        
    def getTopic(self):
        context = Acquisition.aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        topic = portal.restrictedTraverse(self.tp)
        return topic        
        
    def Title(self):
        topic = self.getTopic()
        query = topic.buildQuery()
        subject_vals = list()
        if 'Subject' in query.keys():
            if type(query['Subject'])==type({}) and query['Subject'].has_key('query'):
                subject_vals = query['Subject']['query']
            elif type(query['Subject']) in [StringType, UnicodeType]:
                subject_vals = [query['Subject']]
            elif type(query['Subject']) in [ListType, TupleType]:
                subject_vals = query['Subject']
            subject_vals = [self._t(x, 'osha') for x in subject_vals]

        if 'portal_type' in query.keys():
            if type(query['portal_type']) in [StringType, UnicodeType]:
                portal_types = [query['portal_type']]
            elif type(query['portal_type']) in [ListType, TupleType]:
                portal_types = query['portal_type']
            portal_types = [self._t(x) for x in portal_types]
        else:
            portal_types = []
        
        if 'object_provides' in query.keys():
            if 'slc.publications.interfaces.IPublicationEnhanced' in query['object_provides']:
                portal_types.append(_('Publication'))
            elif type(query['object_provides'])== type({}) and query['object_provides'].has_key('query') and\
                'slc.publications.interfaces.IPublicationEnhanced' in query['object_provides']['query']:
                portal_types.append(_('Publication'))

        if subject_vals and portal_types:
            title = _("header_oshtopic_dynamic", 
                      default = "All ${portal_type} items on ${subject}",
                      mapping=dict(portal_type=', '.join(portal_types), 
                           subject=', '.join(subject_vals))
                     )
        else:
            title = self.getTopic().Title()        
        return title

    def getText(self):
        return self.getTopic().getText()
        
    def Format(self):
        return self.getTopic().Format()        
        
    def queryCatalog(self):
        return self.getTopic().queryCatalog()        

    def getCustomViewFields(self):
        return self.getTopic().getCustomViewFields()
        
    def _t(self, msgid, domain='plone'):
        return translate(domain=domain, msgid=msgid, context=self.context)

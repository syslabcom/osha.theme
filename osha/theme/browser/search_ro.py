import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from types import *
from zLOG import LOG, INFO


class SearchROView(BrowserView):
    """View for displaying the ro filter results
    """
    template = ViewPageTemplateFile('templates/search_ro.pt')
    template.id = "search_ro"
    
    mdelems = ['ero_topic', 'country', 'ero_target_group']
    
    def __call__(self):
        #self.request.set('disable_border', True)
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        self.country = self.request.get('country', '')
        self.ero_topic = self.request.get('ero_topic', '')
        self.ero_target_group = self.request.get('ero_target_group', '')
        
        #self.allvals = portal_catalog.uniqueValuesFor(self.act_md)
        #self.remaining = [x for x in self.mdelems if x!=self.act_md]  # former subsel
        return self.template()


    def sortByTargetGroup(self, results):
        context = Acquisition.aq_inner(self.context)
        if not results:
            return []

        pv = getToolByName(context, 'portal_vocabularies')
        VOCAB = getattr(pv, 'OSHAMetadata', None) 
        vocabDict = VOCAB.getVocabularyDict(VOCAB)
        ETG = vocabDict.get('ero_target_group', [])
        tgs = ETG[1].keys()

        sortedlist = []
        sortmap = {}
    
        
        for r in results:
            OMD = r.getOsha_metadata
            if not OMD:
                continue
            md = list()
            for elem in OMD:
                if elem.find('::'):
                    key, val = elem.split('::')
                    if key=='ero_target_group':
                        md.append(elem)
            if not len(md):
                continue
        
            for m in md:
                if not sortmap.has_key(m):
                    sortmap[m]=[]
                sortmap[m].append(r)

        for tg in tgs:
            if sortmap.has_key(tg):
                sp = sortmap[tg]
                sp.sort(lambda x, y: cmp(x.Title.lower(), y.Title.lower()))
                for s in sp:
                    sortedlist.append(s)
        
        return sortedlist


    def results(self):
        """ query the catalog """
        context = Acquisition.aq_inner(self.context)
        portal_catalog = getToolByName(context, 'portal_catalog')
        if not self.country:
            mdq =  {'query' : ('ero_topic::%s'%self.ero_topic, 'ero_target_group::%s'%self.ero_target_group),
                    'operator': 'and'}
        else:
            if self.ero_target_group:
                mdq = ('ero_target_group::%s'%self.ero_target_group, )
            elif self.ero_topic:
                mdq = ('ero_topic::%s'%self.ero_topic,)
        query = {'country':self.country, 
                 'osha_metadata': mdq,
                 'review_state':'published'
                   }
        LOG('osha.theme.search_ro', INFO, 'query: %s' %query)
        results = portal_catalog(query)
        LOG('osha.theme.search_ro', INFO, 'Number of results: %d' %len(results))
        results = self.sortByTargetGroup(results)        
        return results

    def getCN(self, codes):
        """ returns the countryname for the code """
        portal_countryutils = getToolByName(self.context, 'portal_countryutils')
        getCC = portal_countryutils.getCountryByIsoCode
        if not type(codes) in [ListType, TupleType]:
            codes = [codes]
                    
        return ", ".join([getCC(x).name for x in codes]).strip()
        
    def pretty(self, text):
        """ makes a metadatum pretty """
        def _b(text):
            return text.replace('_', ' ').capitalize()
            
        if not type(text) in [ListType, TupleType]:
            text = [text]
                        
        return ", ".join([_b(x) for x in text])

    def title(self):
        """ returns the proper title """

        if not self.country:
            return "%s - %s" % (self.pretty(self.ero_topic), self.pretty(self.ero_target_group))
        elif not self.ero_target_group:
            return "%s - %s" % (self.pretty(self.ero_topic), self.getCN(self.country))                    
        elif not self.ero_topic:
            return "%s - %s" % (self.getCN(self.country), self.pretty(self.ero_target_group))
            

    def getTopicName(self, brain):
        """ returns the topic name extracted from osha_metadata"""
        omd = brain.getOsha_metadata
        topic_name = ''
        for elem in omd:
            if elem.find('::'):
                key, val = elem.split('::')
                if key=='ero_topic':
                    topic_name=val
                    break
        return topic_name
                      

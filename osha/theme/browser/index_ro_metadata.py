import Acquisition
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter

class IndexROMetadataView(BrowserView):
    """View for displaying the ro content filter page 
    """
    template = ViewPageTemplateFile('templates/index_ro_metadata.pt')
    template.id = "index_ro_metadata"
    
    mdelems = ['getEroTopic', 'country', 'getEroTargetGroup']
    
    def __call__(self):
        #self.request.set('disable_border', True)
        self.act_md = self.request.get('act_md', '')
        self.act_mdval = self.request.get('act_mdval', '')
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        
        self.allvals = portal_catalog.uniqueValuesFor(self.act_md)
        self.remaining = [x for x in self.mdelems if x!=self.act_md]  # former subsel
        return self.template()

    def pretty(self, text):
        """ makes a metadatum pretty """
        return text.replace('_', ' ').capitalize()

    def title(self):
        """ returns the proper title """
        portal_countryutils = getToolByName(self.context, 'portal_countryutils')
        if self.act_md in ['getEroTopic', 'getEroTargetGroup']:
            return self.pretty(self.act_mdval)
        elif self.act_md == 'country':
            return portal_countryutils.getCountryByIsoCode(self.act_mdval).name
        else:
            return ''   

    def findDistinctValues(self, act_md, act_mdval):
        """ search the catalog for all entries which are within the riskob and match the given keyword """
        portal_catalog = getToolByName(self.context, 'portal_catalog')
        portal_countryutils = getToolByName(self.context, 'portal_countryutils')
        
        portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
        navigation_root_path = portal_state.navigation_root_path()
        
        query = {act_md: act_mdval,
                 'Language': 'all',
                 'review_state': 'published'
                    }
        results = portal_catalog(query)
        TO = set()
        CO = set()
        TG = set()
        for result in results:
            if result['getEROTopic']:
                TO = TO.union(result['getEROTopic'])
            if result['getCountry']:
                CO = CO.union(result['getCountry'])                    
            if result['getEROTarget_group']:
                TG = TG.union(result['getEROTarget_group'])            

        TO = list(TO)
        CO = list(CO)
        TG = list(TG)
        
        COS = []        
        path = self.context.absolute_url()+"/search_ro?"+act_md+'='+act_mdval+'&country=%s'  
        for country in CO:
            COS.append((portal_countryutils.getCountryByIsoCode(country).name, country, path%country)) 
        COS.sort(lambda x,y: cmp(x[0], y[0]))

        TGS = []
        path = self.context.absolute_url()+"/search_ro?"+act_md+'='+act_mdval+'&getEroTargetGroup=%s'  
        for tg in TG:
            tgn = self.pretty(tg)
            TGS.append((tgn, tg, path%tg))
        TGS.sort(lambda x,y: cmp(x[0], y[0]))

        TOS = []
        path = self.context.absolute_url()+"/%s/search_ro?"+act_md+'='+act_mdval+'&getEroTopic=%s'  
        for to in TO:
            ton = self.pretty(to)
            TOS.append((ton, to, path%(to, to)))
        TOS.sort(lambda x,y: cmp(x[0], y[0]))
        
        return {'getEroTopic': TOS, 
                'country': COS, 
                'getEroTargetGroup': TGS}
                        
                        
    def summary(self):
        """ check if summary exists and return its description if so """
        if self.act_md=='getEroTopic' and 'summary_html' in self.context.objectIds():
            s = getattr(self.context, 'summary_html')
            desc = s.Description().strip()
            if desc.startswith('Summary'):
                desc = desc[7:]
            return desc
        return False
                    
    def summary_more(self):
        """ check if summary has bodytext and return more link if so """
        if 'summary_html' in self.context.objectIds():
            s = getattr(self.context, 'summary_html')
            if s.getText().strip()!='':
                return s.absolute_url()
        return False                                  

#    def search_portal_types(self):
#        """ compute the list of query params to search for portal_types"""
#        context = Acquisition.aq_inner(self.context)    
#        query = {}       
#        query.update({'portal_type': 'RichDocument'})
#        return query
#        
#    def buildQuery(self):
#        """ Build the query based on the request """
#        context = Acquisition.aq_inner(self.context)
#        query = { 'sort_on': 'effective',
#                  'sort_order':'reverse',
#                  'Language': ''}
#
#                  
#
#        ero_topic = self.request.get('ero_topic', None)
#        if ero_topic:
#            query.update({'ero_topic':ero_topic})
#
#        ero_target_group = self.request.get('ero_target_group', None)
#        if ero_target_group:
#            query.update({'ero_target_group':ero_target_group})
#
#        country = self.request.get('country', '')
#        if country:
#            query.update({'country':country})
#
#        SearchableText = self.request.get('SearchableText', '')
#        if SearchableText != '':
#            query.update({'SearchableText':{'query':SearchableText, 'ranking_maxhits': 10000}})
#
#        search_portal_types = self.search_portal_types()
#        query.update(search_portal_types)
#
#        return query
#        
#        
#
#    def results(self):
#        """ build the query and do the search """
#        context = Acquisition.aq_inner(self.context)
#        portal_catalog = getToolByName(context, 'portal_catalog')
#        query = self.buildQuery()
#        results = portal_catalog(query)
#        return results
                      
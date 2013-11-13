from django.utils.translation import ugettext_lazy as _
from horizon import tables
from django.views.generic import TemplateView
from . import tables as project_tables
import re

import pysolr

# TODO(DZ): Begin using log as we move to Hawana
# from openstack_dashboard.openstack.common import log as logging
# LOG = logging.getLogger(__name__)

FACETFIELDS = ("project", "user", "host", "image", "power")
INDEXLIMIT = 5
LIMIT = 20

class SearchIndexView(tables.MultiTableView):
    table_classes = (project_tables.AdminHypervisorsTable, project_tables.AdminInstancesTable)
    template_name = 'admin/search/index.html'
    
    # TODO: Get table verbose_name from Meta
    # def get_table(self):
    #     self.table = super(SearchIndexView, self).get_table()
    #     self.title = self.table._meta.verbose_name;
    #     return self.table
    
    def get_context_data(self, **kwargs):
        context = super(SearchIndexView, self).get_context_data(**kwargs)
        context['view'] = self
        return context
    
    def has_more_data(self, table):
        numresults = (self.request.GET.get('type', '') == '' and INDEXLIMIT or LIMIT) * (int(self.request.GET.get('page', 0)) + 1)
        return (isinstance(table, project_tables.AdminHypervisorsTable) and self.hypervisorhits or self.instancehits) > numresults
    
    def get_instances_data(self):
        if self.request.GET.get('type', '') == '' or self.request.GET.get('type') == 'instances':
            solr = pysolr.Solr('http://localhost:8983/solr/vm/', timeout=10)
        
            try:
                instances = solr.search(self.request.GET.get('query') or '*:*', **{
                    "start": LIMIT * int(self.request.GET.get('page', 0)),
                    "rows": self.request.GET.get('type', '') == '' and INDEXLIMIT or LIMIT,
                    "facet": 'true',
                    "facet.field": FACETFIELDS,
                    "fq": [" or ".join(["%s:%s" % (re.escape(name), re.escape(param)) for param in self.request.GET.getlist(name)]) for name in FACETFIELDS if self.request.GET.get(name)]
                })
                self.instancehits = instances.hits
                self.instanceresults = len(instances.docs)
                facets = instances.facets.get("facet_fields")
                self.facets = []
                for field in FACETFIELDS:
                    self.facets.append((field, sorted((facets[field][i], facets[field][i+1]) for i in xrange(0, len(facets[field]), 2))))
            except pysolr.SolrError:
                instances = None
                self.facets = []
                self.instancehits = 0
                self.instanceresults = 0
            
            self._tables.get('instances')._meta.verbose_name = _("Instances (%d)" % self.instancehits)
            
            return instances and instances.docs or []
        else:
            self.facets = []
            self.instancehits = 0
            self.instanceresults = 0
            return []
    
    def get_hypervisors_data(self):
        if self.request.GET.get('type', '') == '' or self.request.GET.get('type') == 'hypervisors':
            solr = pysolr.Solr('http://localhost:8983/solr/host/', timeout=10)
        
            try:
                hosts = solr.search(self.request.GET.get('query') or '*:*', **{
                    "start": LIMIT * int(self.request.GET.get('page', 0)),
                    "rows": self.request.GET.get('type', '') == '' and INDEXLIMIT or LIMIT,
                })
                self.hypervisorhits = hosts.hits
                self.hypervisorresults = len(hosts.docs)
            except pysolr.SolrError:
                hosts = None
                self.hypervisorhits = 0
                self.hypervisorresults = 0
            
            self._tables.get('hypervisors')._meta.verbose_name = _("Hypervisors (%d)" % self.hypervisorhits)
            
            return hosts and hosts.docs or []
        else:
            self.hypervisorhits = 0
            self.hypervisorresults = 0
            return []

from django.utils.translation import ugettext_lazy as _
from horizon import tables
from openstack_dashboard.dashboards.project.instances \
    import tables as project_tables
from django.core.urlresolvers import reverse

# TODO(DZ): Begin using log as we move to Havana
#from openstack_dashboard.openstack.common import log as logging
#LOG = logging.getLogger(__name__)


class AdminHypervisorsTable(tables.DataTable):
    def get_object_id(self, datum):
        return datum["id"]
    
    def get_pagination_string(self):
        """ Returns the query parameter string to paginate this table. """
        
        list = ["&".join(["%s=%s" % (name, param) for param in self.request.GET.getlist(name)]) for name in self.request.GET if name != self._meta.pagination_param and name != 'type']
        if not self.request.GET.get("type", '') == '':
            list.append("=".join([self._meta.pagination_param, str(int(self.request.GET.get("page", 0)) + 1)]))
        list.append("type=hypervisors")
        
        return "&".join(list)
    
    name = tables.Column("name",
                         link=("/admin/hypervisors/"),
                         verbose_name=_("Name"))
    hypervisor = tables.Column("hypervisor", verbose_name=_("Hypervisor"))
    vcpus = tables.Column("vcpus",
                          verbose_name=_("VCPUs"))
    memory = tables.Column("memory",
                           verbose_name=_("Memory"))
    storage = tables.Column("storage",
                            verbose_name=_("Storage"))
    vm_count = tables.Column("vm_count",
                             verbose_name=_("No. of instances"))
    
    class Meta:
        name = "hypervisors"
        verbose_name = _("Hypervisors")
        pagination_param = "page"

class AdminInstancesTable(tables.DataTable):
    def get_object_id(self, datum):
        return datum["id"]
    
    def get_pagination_string(self):
        """ Returns the query parameter string to paginate this table. """
        
        list = ["&".join(["%s=%s" % (name, param) for param in self.request.GET.getlist(name)]) for name in self.request.GET if name != self._meta.pagination_param and name != 'type']
        if not self.request.GET.get("type", '') == '':
            list.append("=".join([self._meta.pagination_param, str(int(self.request.GET.get("page", 0)) + 1)]))
        list.append("type=instances")
        
        return "&".join(list)
    
    name = tables.Column("name",
                         link=("horizon:admin:instances:detail"),
                         verbose_name=_("Name"))
    tenant = tables.Column("project", verbose_name=_("Project"))
    host = tables.Column("host",
                         verbose_name=_("Host"),
                         classes=('nowrap-col',))
    image_name = tables.Column("image",
                               verbose_name=_("Image Name"))
    flavor = tables.Column("flavor",
                           verbose_name=_("Flavor"))
    state = tables.Column("state",
                          verbose_name=_("State"))
    power = tables.Column("power",
                          verbose_name=_("Power"))
    uptime = tables.Column("uptime",
                           verbose_name=_("Uptime"))
    class Meta:
        name = "instances"
        verbose_name = _("Instances")
        pagination_param = "page"

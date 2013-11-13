from django.utils.translation import ugettext_lazy as _

import horizon

from openstack_dashboard.dashboards.admin import dashboard


class Search(horizon.Panel):
    name = _("Search")
    slug = 'search'


dashboard.Admin.register(Search)
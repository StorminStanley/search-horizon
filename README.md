search-horizon
==============

Brings full text search to Horizon dashboard for OpenStack admin. A prototype. 


Install
-------

1. Install module to pythonpath

    sudo pip install -e git+https://github.com/StackStorm/search-horizon.git#egg=search-horizon

2. Edit local_settings.py (`$HORIZON_DIR/openstack_dashboard/local/local_settings.py` when installed from sources; `/etc/openstack-dashboard/local_settings.py` when installed on Ubuntu/Debian. Add ```customization_module``` param to HORIZON_CONFIG.

    HORIZON_CONFIG = {
      ...
      "customization_module": "search.overrides"
    }

3. Make sure search servcie is running and filling up solr with data. See [StackStorm/search](https://github.com/StackStorm/search)

4. Edit solr url in search/search/tables.py if needed (yes it's a hack for now, TODO: move out to configuration).

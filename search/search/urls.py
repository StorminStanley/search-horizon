from django.conf.urls.defaults import patterns, url
from .views import SearchIndexView

urlpatterns = patterns('',
    url(r'^$', SearchIndexView.as_view(), name='index')
)

_author__ = 'mstacy'
from django.conf.urls import patterns, url
from catalog.views import SourceList, SourceDetail
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
                       url(r'^source/$', SourceList.as_view(), name='source-list'),
                       url(r'^source/(?P<id>[^/]+)/$', SourceDetail.as_view(), name='source-detail'),

)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'jsonp', 'xml', 'yaml'])
print urlpatterns
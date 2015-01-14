__author__ = 'mstacy'
from django.conf.urls import patterns, url
from data_store.views import MongoDataStore, DataStore
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = patterns('',
                       url(r'^data/$', MongoDataStore.as_view(), name='data-list'),
                       url(r'^data/(?P<database>[^/]+)/$', MongoDataStore.as_view(), name='data-list'),
                       url(r'^data/(?P<database>[^/]+)/(?P<collection>[^/]+)/$', DataStore.as_view(),
                           name='data-detail'),
                       #url(r'^data/(?P<database>[^/]+)/$', MongoDataStore.as_view(), name='source-detail'),


)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['api', 'json', 'jsonp', 'xml', 'yaml'])
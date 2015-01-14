from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views import APIRoot, UserProfile, UserDetail, AuthToken

admin.autodiscover()

urlpatterns = patterns('',
    # Django Rest Login Urls
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Queue Application
    url(r'^queue/', include('queue.urls')),
    url(r'^catalog/', include('catalog.urls')),
    url(r'^data_store/',include('data_store.urls')),
    # Admin Urls
    url(r'^admin/', include(admin.site.urls)),
    # Main Project View - Customize depending on what Apps are enabled
    url(r'^$', APIRoot.as_view()),
    url(r'^/\.(?P<format>(api|json|jsonp|xml|yaml))/$', APIRoot.as_view()),
    url(r'^user/',UserProfile.as_view(),name='user-list'),
    url(r'^user/(?P<id>[0-9]+)/$',UserDetail.as_view(),name='user-detail'),
    #url(r'^usertoken/', AuthToken.as_view(), name='token-detail'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

)
#urlpatterns1 = patterns(url(r'^$', APIRoot.as_view()),
#    url(r'^/\.(?P<format>(api|json|jsonp|xml|yaml))/$', APIRoot.as_view()),)

#print urlpatterns1
#urlpatterns = format_suffix_patterns(, allowed=['api','json','jsonp', 'xml','yaml'])
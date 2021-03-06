from django.conf.urls import patterns, include, url
from django.contrib import admin
import twitter_auth.views
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', twitter_auth.views.main, name='main'),
    url(r'^accounts/twitter/login/callback/$', twitter_auth.views.callback, name='auth_return'),
    url(r'^logout/$', twitter_auth.views.unauth, name='oauth_unauth'),
    url(r'^auth/$', twitter_auth.views.auth, name='oauth_auth'),
    url(r'^info/$', twitter_auth.views.info, name='info'),
    url(r'^location/$', twitter_auth.views.location),
    url(r'^locationupdate/$', twitter_auth.views.location_updater),
    
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
   
    url(r'^admin/', include(admin.site.urls)),
    url(r'^loc/(?P<username>\w+)/$', twitter_auth.views.locationshuffle),
    url(r'^(?P<username>\w+)/$',     twitter_auth.views.userprofile)
)

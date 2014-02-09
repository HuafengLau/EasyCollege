from django.conf.urls.defaults import *

urlpatterns = patterns('Business.views',
    url(r'^guide/getCreditFile/(?P<school_code>.+)/$', 'guide_getCreditFile', name='guide_getCreditFile'),
)
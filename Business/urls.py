from django.conf.urls.defaults import *

urlpatterns = patterns('Business.views',
    url(r'^about/$', 'about', name='business_about'),
    #url(r'^guide/getCreditFile/(?P<school_code>.+)/$', 'guide_getCreditFile', name='guide_getCreditFile'),
    #url(r'TheRich/$', 'TheRich', name='TheRich'),
)
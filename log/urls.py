from django.conf.urls.defaults import *

urlpatterns = patterns('log.views',
    url(r'^$', 'log', name='log'),
    url(r'^activate/(?P<id>\d+)/', 'activateUser', name='activateUser'),
    url(r'^logout/$', 'quit', name='log_quit'),
    url(r'^page_register/$', 'page_register', name='page_register'),
    url(r'^register/$', 'register', name='register')
)
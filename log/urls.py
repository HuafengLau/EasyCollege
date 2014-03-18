from django.conf.urls.defaults import *

urlpatterns = patterns('log.views',
    url(r'^$', 'log', name='log'),
    url(r'^activate/(?P<id>\d+)/', 'activateUser', name='activateUser'),
    url(r'^logout/$', 'quit', name='log_quit'),
    url(r'^page_register/$', 'page_register', name='page_register'),
    #url(r'^page_register1/$', 'page_register1', name='page_register'),
    #url(r'^page_register2/$', 'page_register2', name='page_register'),
    url(r'^verify_email/$', 'verify_email', name='register_verify_email'),
    url(r'^register/step1/$', 'deal_register', name='deal_register'),
   # url(r'^register/step3/$', 'register_step3', name='register_step3')
)
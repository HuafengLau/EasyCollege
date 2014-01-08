from django.conf.urls.defaults import *

urlpatterns = patterns('Center.views',
    url(r'^$', 'center', name='center'),
    url(r'^delStore/(?P<eot_id>\d+)/$', 'delStore', name='Center_delStore')
    #url(r'^collect/(?P<credit_id>\d+)/$', 'showcredit', name='eot_showcredit'),
)
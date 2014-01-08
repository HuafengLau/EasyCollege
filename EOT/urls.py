from django.conf.urls.defaults import *

urlpatterns = patterns('EOT.views',
    url(r'^$', 'list', name='eot_list'),
    url(r'^showcredit/(?P<credit_id>\d+)/$', 'showcredit', name='eot_showcredit'),
    url(r'^showeot/(?P<eot_id>\d+)/$', 'showeot', name='eot_showeot'),
    url(r'^value/test/$', 'test', name='test'),
    url(r'^value/(?P<credit_id>\d+)/$', 'value', name='eot_value'),    
    url(r'^list/$', 'list', name='eot_list'),
    url(r'^poll/$', 'poll', name='eot_poll'),
    url(r'^search/$', 'search', name='eot_search'),
    url(r'^search/sort/$', 'search_sort', name='eot_search_sort'),
    url(r'^uploadfile/(?P<eot_id>\d+)/$', 'uploadfile', name='eot_uploadfile'),
    url(r'^uploadImg/(?P<eot_id>\d+)/$', 'uploadImg', name='eot_uploadImg'),
    url(r'^downloadfile/(?P<data_id>\d+)/(?P<path>.{8,100})/$', 'downloadfile', name='eot_downloadfile'),
    url(r'^showcomment/(?P<Eotdata_id>\d+)/$', 'showcomment', name='eot_showcomment'),
    url(r'^commentdata/(?P<Eotdata_id>\d+)/$', 'comment_Eotdata', name='eot_comment_Eotdata'),
    url(r'^store/$', 'store_eot', name='eot_store'),
    url(r'^delStore/$', 'delStore', name='eot_delStore')
)
from django.conf.urls.defaults import *

urlpatterns = patterns('Index.views',
    url(r'^$', 'index', name='index'),
    #url(r'^wise_teacher/$', 'wise_teacher', name='wise_teacher'),
    #url(r'^delete/(?P<credit_id>\d+)/$', 'del_credit', name='del_credit'),
    url(r'^get_idCard/$', 'get_idCard', name='get_idCard'),
    #url(r'verify_URP/$', 'verify_URP', name='index_verify_URP'),
    url(r'loading_gif/$', 'loading_gif', name='loading_gif'),
    #url(r'URP_getCredit/$', 'URP_getCredit', name='URP_getCredit'),
    #url(r'wise_getCredit/(?P<school_code>.+)/$', 'wise_getCredit', name='wise_getCredit'),
)
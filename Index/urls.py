from django.conf.urls.defaults import *

urlpatterns = patterns('Index.views',
    url(r'^$', 'index', name='index'),
    url(r'^wise_teacher/$', 'wise_teacher', name='wise_teacher'),
    url(r'^delete/(?P<credit_id>\d+)/$', 'del_credit', name='del_credit'),
    url(r'^uploadavatar/$', 'upload_avatar', name='upload_avatar')
)
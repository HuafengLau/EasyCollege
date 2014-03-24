from django.conf.urls.defaults import *

urlpatterns = patterns('account.views',
    url(r'^QQlogin/$', 'QQ_login', name='account_QQ_login'),
)
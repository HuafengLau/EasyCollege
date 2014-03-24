from django.conf.urls.defaults import *

urlpatterns = patterns('account.views',
    url(r'^QQlogin/$', 'QQ_login', name='account_QQ_login'),
    url(r'^(?P<openid>.+)/$', 'testQQlog', name='account_QQ_testQQlog'),
)
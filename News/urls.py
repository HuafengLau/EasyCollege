from django.conf.urls.defaults import *

urlpatterns = patterns('News.views',
    url(r'^$', 'news', name='news_all_all'),
    url(r'(?P<news_interest>.+)/(?P<news_part>.+)/$', 'which_news', name='which_news'),
)
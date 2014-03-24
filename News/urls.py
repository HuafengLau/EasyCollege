from django.conf.urls.defaults import *

urlpatterns = patterns('News.views',
    url(r'^$', 'news', name='news_all_all'),
    url(r'^submitPic/$', 'submitPic', name='news_submitPic'),
    url(r'^getTopPart/$','getTopPart',name='news_GetTopPart'),
    url(r'^giveGold/$', 'giveGold', name='news_giveGold'),
    url(r'^watch/$', 'watch', name='news_watch'),
    url(r'^reply/$', 'reply', name='news_reply'),
    url(r'^uploadTextPic/$', 'ke_upload_view', name='news_ke_upload_view'),
    url(r'^mySubscription/$', 'mySubscription', name='news_mySubscription'),
    url(r'^comment/$', 'comment', name='news_comment'),
    url(r'^vote/$', 'newsVote', name='news_newsVote'),
    url(r'^comment/vote/$', 'commentVote', name='news_commentVote'),
    url(r'^(?P<news_part>.+)/(?P<small_part>.+)/showNews/(?P<news_id>\d+)/$', 'show_news', name='show_news'),
    url(r'^(?P<news_part>.+)/submit/(?P<news_type>\w{3,5})/$', 'submit_news', name='submit_news'),
    url(r'^(?P<news_part>.+)/(?P<small_part>.+)/$', 'which_news', name='which_news'),
)
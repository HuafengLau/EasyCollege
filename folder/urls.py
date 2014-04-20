from django.conf.urls.defaults import *

urlpatterns = patterns('folder.views',
    url(r'^$', 'folder', name='folder'),
    url(r'^newBuild/$', 'newBuild', name='folder_newBuild'),
    url(r'^collect/$', 'collect', name='folder_collect'),
    url(r'^watch/$', 'watch', name='folder_watch'),
)
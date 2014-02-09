#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from log.views import log, verify
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EasyCollege.views.home', name='home'),
    # url(r'^EasyCollege/', include('EasyCollege.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^log/', include('log.urls')),
    url(r'^index/', include('Index.urls')),
    url(r'^eot/', include('EOT.urls')),
    url(r'^center/', include('Center.urls')),
    url(r'^affair/', include('Affair.urls')),
    url(r'^business/', include('Business.urls')),
    (r'^$', log),  
    (r'^verify/$', verify),
    (r'^appmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT})
)

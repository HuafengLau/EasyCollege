#coding:utf-8

from django.conf.urls import patterns, include, url
from django.contrib import admin
from log.views import log, verify
from Business.views import googelSearch, baiduSearch
from django.conf import settings
from django.views.generic import TemplateView
from EOT.models import Eot

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
    (r'^robots\.txt$', TemplateView.as_view(template_name= 'robots.txt', content_type='text/plain')),
    (r'^sitemaps1\.xml$', TemplateView.as_view(template_name= 'sitemaps1.xml', content_type='text/plain')),
    (r'^googlee7b5e63c07c5ed83.html/$', googelSearch),
    (r'^baidu_verify_hWg7x7b1q5.html/$', baiduSearch),
    (r'^verify/$', verify),
    (r'^appmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT})
)

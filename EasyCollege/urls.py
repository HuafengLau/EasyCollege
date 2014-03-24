#coding:utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from News.views import fangqiu,upload,upload_delete
from log.views import verify
from Business.views import googelSearch, baiduSearch,baiduSearch2,googelSearch2
from django.conf import settings
from django.views.generic import TemplateView
#from EOT.models import Eot

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
    #url(r'^eot/', include('EOT.urls')),
    url(r'^center/', include('Center.urls')),
    url(r'^affair/', include('Affair.urls')),
    url(r'^business/', include('Business.urls')),
    url(r'^news/', include('News.urls')),
    url( r'upload/', upload, name = 'jfu_upload' ),  
    url( r'^delete/(?P<pk>\d+)/$', upload_delete, name = 'jfu_delete' ),
    (r'^$', fangqiu),
    (r'^robots\.txt$', TemplateView.as_view(template_name= 'robots.txt', content_type='text/plain')),
    (r'^sitemaps1\.xml$', TemplateView.as_view(template_name= 'sitemaps1.xml', content_type='text/plain')),
    (r'^googlee7b5e63c07c5ed83.html/$', googelSearch),
    (r'^googlee7b5e63c07c5ed83.html/$', googelSearch2),
    (r'^baidu_verify_e7gA3p0lSA.html/$',baiduSearch2),
    (r'^baidu_verify_hWg7x7b1q5.html/$', baiduSearch),
    (r'^verify/$', verify),
    (r'^appmedia/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.STATIC_ROOT})
)

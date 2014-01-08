from django.conf.urls.defaults import *

urlpatterns = patterns('Affair.views',
    url(r'^$', 'affair', name='affair'),
    url(r'^report/eotData/$', 'report_eotData', name='affair_report_eotData'),
    url(r'^report/eotImg/(?P<Report_eotImg_id>\d+)/$', 'report_eotImg', name='affair_report_eotImg'),
    url(r'^handle/report/Report_eotDatas/(?P<eotData_id>\d+)/(?P<dispose>-?\d+)/$', 
        'handle_reportEotData_dispose', name='affair_handle_reportEotData_dispose'),
    url(r'^handle/report/Report_eotImg/(?P<eotImg_id>\d+)/(?P<dispose>-?\d+)/$', 
        'handle_reportEotImg_dispose', name='affair_handle_reportEotImg_dispose'),
    #url(r'^sendEmail/$', 'test_sendEmail', name='affair_test_sendEmail'),
)
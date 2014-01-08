#coding:utf-8

from django.db import models
from account.models import MyUser
from EOT.models import Eot, Eot_data

class Report_eotData(models.Model):
    eot = models.ForeignKey(Eot, null=True,blank=True,on_delete=models.SET_NULL,verbose_name=u'课程')
    eot_data = models.ForeignKey(Eot_data, null=True,blank=True,on_delete=models.SET_NULL,verbose_name=u'课程资料')
    suspect = models.ForeignKey(MyUser, null=True,blank=True,on_delete=models.SET_NULL,related_name='suspects_Report', verbose_name=u'被举报者')
    reporter = models.ForeignKey(MyUser, null=True,blank=True,on_delete=models.SET_NULL,related_name='reporters_Report', verbose_name=u'举报者')
    solve_time = models.DateField(blank=True, null=True, verbose_name=u'解决时间')
    report_time = models.DateField(auto_now_add=True, null=True, verbose_name=u'举报时间')
    result = models.CharField(max_length=10)
    
    def __unicode__(self):
        return self.id
    
    class Meta:
        ordering = ['report_time','result']
        verbose_name = u'资料举报'
        verbose_name_plural = u'资料举报'
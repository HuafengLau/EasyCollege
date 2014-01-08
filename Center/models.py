#coding:utf-8

from account.models import MyUser
from django.db import models

class User_info(models.Model):
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'用户')
    store_eot = models.CharField(max_length=250,null=True,blank=True,verbose_name=u'收藏的课程')    
    download_Eotdata = models.CharField(max_length=250,null=True, blank=True,verbose_name=u'下载的资料')
    nocomment_Eotdata = models.CharField(max_length=250,null=True, blank=True, verbose_name=u'未评价资料')
    
    def __unicode__(self):
        return self.user
    
    class Meta:
        ordering = ['user',]
        verbose_name = u'用户信息'
        verbose_name_plural = u'用户信息'

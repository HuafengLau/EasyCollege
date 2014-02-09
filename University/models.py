#coding:utf-8

from django.db import models

class University_info(models.Model):
    school = models.CharField(max_length=30,verbose_name=u'学校')
    college = models.CharField(max_length=30, verbose_name=u'学院')
    major = models.CharField(max_length=40, verbose_name=u'专业')
    
    def __unicode__(self):
        return '%s,%s,%s' %(self.school, self.college, self.major)
    
    class Meta:
        ordering = ['school',]
        verbose_name = u'院校信息'
        verbose_name_plural = u'院校集'
    


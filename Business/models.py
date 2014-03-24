#coding:utf-8

from django.db import models
from account.models import MyUser
from University.models import University_info

class AuthorLog(models.Model):
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'用户')
    openid =  models.CharField(max_length=100,null=True,verbose_name=u'授权id')
    type = models.CharField(max_length=20,null=True,verbose_name=u'授权类型')

    def __unicode__(self):
        return '%s' % self.openid
        
    class Meta:
        #ordering = ['grade',]
        verbose_name = u'授权登录'
        verbose_name_plural = u'授权登录'
    
class Credit(models.Model):
    course_name = models.CharField(max_length=100,null=True,verbose_name=u'课程名')
    course_teacher = models.CharField(max_length=100,null=True, blank=True,verbose_name=u'任课老师')
    course_credit = models.FloatField(verbose_name=u'学分')
    course_attr = models.CharField(max_length=100,null=True,verbose_name=u'课程属性')
    course_score = models.FloatField(verbose_name=u'成绩')
    add_money = models.IntegerField(verbose_name=u'评教奖励')
    grade = models.CharField(max_length=20,null=True,verbose_name=u'年级')
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'用户')
    university_info_id = models.CharField(max_length=30,null=True,verbose_name=u'院校id')
    add_date = models.DateField(auto_now_add=True, null=True,verbose_name=u'添加时间')
    
    
    def __unicode__(self):
        return '%s,%s' %(self.course_name, self.id)
        
    class Meta:
        #ordering = ['grade',]
        verbose_name = u'成绩单'
        verbose_name_plural = u'成绩'
        
class Major_course(models.Model):
    course = models.ForeignKey(Credit, null=True,verbose_name=u'课程')
    course_name = models.CharField(max_length=30, null=True, verbose_name=u'课程名称')
    course_teacher = models.CharField(max_length=30, null=True, verbose_name=u'任课老师')
    major_id = models.CharField(max_length=30,null=True,verbose_name=u'院校id')
    
    def __unicode__(self):
        return '%s, %s, %s' % (self.major_id, self.course_name, self.course_teacher)
        
    class Meta:
        ordering = ['major_id', ]
        verbose_name = u'专业课程集'
        verbose_name_plural = u'专业课程'
#coding:utf-8
from django.db import models
from account.models import MyUser

class News(models.Model):
     user = models.ForeignKey(MyUser, null=True,verbose_name=u'发表用户')
     
     type = models.CharField(max_length=10,null=True,verbose_name=u'类型')
     title = models.CharField(max_length=100,null=True,verbose_name=u'标题')
     url = models.URLField(null=True,verbose_name=u'链接')
     text = models.TextField(null=True,verbose_name=u'文本')
     part = models.CharField(max_length=100,null=True,verbose_name=u'板块')
     
     ups = models.IntegerField(default=0,null=True,verbose_name=u'顶')
     downs = models.IntegerField(default=0,null=True,verbose_name=u'沉')
     
     time = models.DateTimeField(auto_now_add=True,verbose_name=u'发表时间')
     gold = models.IntegerField(default=0,null=True,verbose_name=u'赏金')
     score = models.IntegerField(default=0,null=True,verbose_name=u'得分')
     controversy = models.FloatField(null=True,verbose_name=u'争议得分')
     hot = models.FloatField(null=True,verbose_name=u'热度得分')
     
     def __unicode__(self):
        return 'news_%s_%s' % (self.id,self.time)
    
     class Meta:
        #ordering = ['eot',]
        verbose_name = u'新闻'
        verbose_name_plural = u'新闻'
        
class NewsPart(models.Model):
    part = models.CharField(max_length=100,null=True,verbose_name=u'板块')
    realPart = models.CharField(max_length=100,null=True,verbose_name=u'中文板块')
    num = models.IntegerField(default=0,null=True,verbose_name=u'新闻数')
    
    def __unicode__(self):
        return '%s_%s' % (self.part,self.num)
    
    class Meta:
        ordering = ['num',]
        verbose_name = u'子版块'
        verbose_name_plural = u'子版块'
#coding:utf-8

from account.models import MyUser
from django.db import models

class User_info(models.Model):
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'用户')
    store_eot = models.CharField(max_length=250,null=True,blank=True,verbose_name=u'收藏的课程')    
    download_Eotdata = models.CharField(max_length=250,null=True, blank=True,verbose_name=u'下载的资料')
    nocomment_Eotdata = models.CharField(max_length=250,null=True, blank=True, verbose_name=u'未评价资料')
    grade = models.CharField(max_length=250,null=True, blank=True,verbose_name=u'等级')
    show_email = models.BooleanField(default=True,verbose_name=u'是否显示email')
    sign = models.CharField(max_length=50,default=u'ta什么也没说',verbose_name=u'个性签名')
    upVoted_news = models.TextField(default='',blank=True,verbose_name=u'支持的分享')
    downVoted_news = models.TextField(default='',blank=True,verbose_name=u'不支持的分享')
    beWatched = models.TextField(default='',blank=True,verbose_name=u'被关注')
    watching = models.TextField(default='',blank=True,verbose_name=u'关注')
    subscription = models.TextField(default='ExplainCY;Funny;Home-news;Life;AskAnything;',blank=True,verbose_name=u'收藏的社群')
    upVoted_comment1 = models.TextField(default='',blank=True,verbose_name=u'赞同评论1')
    upVoted_comment2 = models.TextField(default='',blank=True,verbose_name=u'赞同评论2')
    upVoted_comment3 = models.TextField(default='',blank=True,verbose_name=u'赞同评论3')
    upVoted_comment4 = models.TextField(default='',blank=True,verbose_name=u'赞同评论4')
    downVoted_comment1 = models.TextField(default='',blank=True,verbose_name=u'不赞同评论1')
    downVoted_comment2 = models.TextField(default='',blank=True,verbose_name=u'不赞同评论2')
    downVoted_comment3 = models.TextField(default='',blank=True,verbose_name=u'不赞同评论3')
    downVoted_comment4 = models.TextField(default='',blank=True,verbose_name=u'不赞同评论4')
    when_newsbeGold = models.CharField(max_length=20,default=u'你的支持是我分享的动力：）', blank=True,verbose_name=u'回应分享镀金')
    when_commentbeGold = models.CharField(max_length=20,default=u'下一次，我的评论将更有含金量：）', blank=True,verbose_name=u'回应评论镀金')
    #when_beAgreed = models.CharField(max_length=20,default=u'感谢赞同：）', blank=True,verbose_name=u'回应赞同')
    when_beWatched = models.CharField(max_length=20,default=u'感谢关注：）', blank=True,verbose_name=u'回应关注')
    agree_num = models.IntegerField(default=0,blank=True,verbose_name=u'获赞')

    def __unicode__(self):
        return self.user
    
    class Meta:
        ordering = ['user',]
        verbose_name = u'用户信息'
        verbose_name_plural = u'用户信息'
        
class Honour(models.Model):
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'用户')
    img = models.CharField(max_length=20,null=True, blank=True,verbose_name=u'荣誉图片')
    info = models.CharField(max_length=50,null=True, blank=True,verbose_name=u'说明')
    
    def __unicode__(self):
        return self.user
    
    class Meta:
        ordering = ['user',]
        verbose_name = u'用户荣誉'
        verbose_name_plural = u'用户荣誉'

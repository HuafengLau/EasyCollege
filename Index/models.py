#coding:utf-8

from django.db import models
from account.models import MyUser
from News.models import News,NewsComment1,NewsComment2,NewsComment3,NewsComment4

# Create your models here.
class Avatar(models.Model):
    photo = models.ImageField(upload_to='avatar/',blank=True,null=True)
    user = models.ForeignKey(MyUser,related_name="profile",blank=True,null=True)
    
    def __unicode__(self):
        return '%s' % (self.user)
        
class Feeds_news(models.Model):
    type = models.CharField(max_length=30,blank=True,verbose_name=u'动态类型')
    showText = models.BooleanField(default=True,blank=True,verbose_name=u'显示文本')
    owner = models.ForeignKey(MyUser,related_name='ownerFNews',blank=True,null=True,verbose_name=u'拥有者')
    creator = models.ForeignKey(MyUser,related_name='creatorFNews',blank=True,null=True,verbose_name=u'创造者')
    news = models.ForeignKey(News,blank=True,null=True,verbose_name=u'相关分享')
    
    gold_num = models.IntegerField(default=0,verbose_name=u'镀金')
    comment = models.ForeignKey(NewsComment1,blank=True,null=True,verbose_name=u'相关评论')
    
    time = models.DateTimeField(auto_now=True,verbose_name=u'产生时间')
    
    def __unicode__(self):
        return '%s_%s' % (self.type, self.id)
        
    class Meta:
        ordering = ['time',]
        verbose_name = u'分享动态'
        verbose_name_plural = u'分享动态'
        
class Feeds_comment(models.Model):
    type = models.CharField(max_length=30,blank=True,verbose_name=u'动态类型')
    showText = models.BooleanField(default=False,blank=True,verbose_name=u'显示文本')
    owner = models.ForeignKey(MyUser,related_name='ownerFComment',blank=True,null=True,verbose_name=u'拥有者')
    creator = models.ForeignKey(MyUser,related_name='creatorFComment',blank=True,null=True,verbose_name=u'创造者')
    news = models.ForeignKey(News,blank=True,null=True,verbose_name=u'相关分享')
    newscomment1 = models.ForeignKey(NewsComment1,blank=True,null=True,verbose_name=u'相关评论1')
    newscomment2 = models.ForeignKey(NewsComment2,related_name='FComment2',blank=True,null=True,verbose_name=u'相关评论2')
    newscomment3 = models.ForeignKey(NewsComment3,related_name='FComment3',blank=True,null=True,verbose_name=u'相关评论3')
    newscomment4 = models.ForeignKey(NewsComment4,related_name='FComment4',blank=True,null=True,verbose_name=u'相关评论4')
    
    gold_num = models.IntegerField(default=0,verbose_name=u'镀金')
    comment2 = models.ForeignKey(NewsComment2,related_name='FReply1',null=True,blank=True,verbose_name=u'相关回复')
    comment3 = models.ForeignKey(NewsComment3,related_name='FReply1',null=True,blank=True,verbose_name=u'相关回复')
    comment4 = models.ForeignKey(NewsComment4,null=True,blank=True,verbose_name=u'相关回复')
  
    time = models.DateTimeField(auto_now=True,verbose_name=u'产生时间')
    
    def __unicode__(self):
        return '%s_%s' % (self.type, self.id)
        
    class Meta:
        ordering = ['time',]
        verbose_name = u'评论动态'
        verbose_name_plural = u'评论动态'
        
class Feeds_followNews(models.Model):
    type = models.CharField(max_length=30,blank=True,verbose_name=u'动态类型')
    showText = models.BooleanField(default=True,blank=True,verbose_name=u'显示文本')
    owner = models.ForeignKey(MyUser,related_name='ownerFfollowNews',blank=True,null=True,verbose_name=u'拥有者')
    creator = models.ForeignKey(MyUser,related_name='creatorFfollowNews',blank=True,null=True,verbose_name=u'创造者')
    news = models.ForeignKey(News,blank=True,null=True,verbose_name=u'相关分享')
    time = models.DateTimeField(auto_now_add=True,verbose_name=u'产生时间')
    
    def __unicode__(self):
        return '%s_%s' % (self.type, self.id)
        
    class Meta:
        ordering = ['time',]
        verbose_name = u'关注动态'
        verbose_name_plural = u'关注动态'
        
class Folder(models.Model):
    name = models.CharField(max_length=20,blank=True,null=True,verbose_name=u'收藏夹名')
    description = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'收藏描述')
    owner = models.ForeignKey(MyUser,blank=True,null=True,verbose_name=u'收藏夹作者')
    
    def __unicode__(self):
        return u'%s' % self.name
        
    class Meta:
        ordering = ['owner',]
        verbose_name = u'收藏夹'
        verbose_name_plural = u'收藏夹'
        
class Collect(models.Model):
    folder = models.ForeignKey(Folder,blank=True,null=True,verbose_name=u'收藏夹')
    news = models.ForeignKey(News,blank=True,null=True,verbose_name=u'相关分享')
    
    def __unicode__(self):
        return u'%s_%s' % (self.folder, self.id)
        
    class Meta:
        ordering = ['folder',]
        verbose_name = u'收藏'
        verbose_name_plural = u'收藏'
        
class WatchFolder(models.Model):
    folder = models.ForeignKey(Folder,blank=True,null=True,verbose_name=u'收藏夹')
    user =  models.ForeignKey(MyUser,blank=True,null=True,verbose_name=u'关注者')
    
    def __unicode__(self):
        return u'%s_%s' % (self.folder, self.id)
        
    class Meta:
        ordering = ['folder',]
        verbose_name = u'关注收藏'
        verbose_name_plural = u'关注收藏'
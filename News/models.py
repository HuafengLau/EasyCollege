#coding:utf-8
from django.db import models
from account.models import MyUser

class NewsPart(models.Model):
    part = models.CharField(max_length=100,null=True,verbose_name=u'板块')
    realPart = models.CharField(max_length=100,null=True,verbose_name=u'中文板块')
    open = models.BooleanField(default=True,verbose_name=u'是否公开')
    secret = models.BooleanField(default=False,verbose_name=u'是否秘密')
    num = models.IntegerField(default=0,null=True,verbose_name=u'新闻数')
    user_num = models.IntegerField(default=0,verbose_name=u'订阅人数')
    description = models.CharField(max_length=100,default=u'这里是关于这个版块的一些描述',verbose_name=u'板块描述')
    can_link = models.BooleanField(default=True,verbose_name=u'允许分享链接')
    can_text = models.BooleanField(default=True,verbose_name=u'允许分享文本')
    can_pic = models.BooleanField(default=True,verbose_name=u'允许分享图片')
    can_mp3 = models.BooleanField(default=False,verbose_name=u'允许分享mp3')
    time = models.DateTimeField(auto_now_add=True,verbose_name=u'成立时间')
    
    def __unicode__(self):
        return '%s' % (self.part)
    
    class Meta:
        ordering = ['part',]
        verbose_name = u'社群'
        verbose_name_plural = u'社群'

class News(models.Model):
     user = models.ForeignKey(MyUser, null=True,verbose_name=u'发表用户')
     newspart = models.ForeignKey(NewsPart, null=True,verbose_name=u'社群')
     open = models.BooleanField(default=True,verbose_name=u'是否公开')
     secret = models.BooleanField(default=False,verbose_name=u'是否秘密')
     type = models.CharField(max_length=10,null=True,verbose_name=u'类型') 
     title = models.CharField(max_length=100,null=True,verbose_name=u'标题')
     
     link = models.URLField(null=True,blank=True,verbose_name=u'链接')
     text = models.TextField(null=True,blank=True,verbose_name=u'文本')
     pic = models.ImageField(upload_to='news_pic/',blank=True,null=True,verbose_name=u'图片')
     mp3  = models.ImageField(upload_to='news_mp3/',blank=True,null=True,verbose_name=u'mp3')
     
     ups = models.IntegerField(default=0,null=True,verbose_name=u'顶')
     downs = models.IntegerField(default=0,null=True,verbose_name=u'沉')
     
     time = models.DateTimeField(auto_now_add=True,verbose_name=u'发表时间')
     gold = models.IntegerField(default=0,null=True,verbose_name=u'赏金')
     score = models.IntegerField(default=0,null=True,verbose_name=u'得分')
     controversy = models.FloatField(null=True,verbose_name=u'争议得分')
     hot = models.FloatField(null=True,verbose_name=u'热度得分')
     
     comment_num = models.IntegerField(default=0,verbose_name=u'评论数量')
     
     def __unicode__(self):
        return 'news_%s_%s' % (self.id,self.time)
    
     class Meta:
        #ordering = ['eot',]
        verbose_name = u'分享'
        verbose_name_plural = u'分享'
       
        
class NewsPartRule(models.Model):
    rule = models.TextField(null=True,verbose_name=u'社群公约')
    newspart = models.ForeignKey(NewsPart, null=True,verbose_name=u'社群')
    
    def __unicode__(self):
        return '%s_%s' % (self.newspart,self.id)
    
    class Meta:
        ordering = ['newspart',]
        verbose_name = u'社群公约'
        verbose_name_plural = u'社群公约'
        
class NewsComment1(models.Model):
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'发表用户')
    ups = models.IntegerField(default=0,verbose_name=u'顶')
    downs = models.IntegerField(default=0,verbose_name=u'沉')
    score = models.IntegerField(default=0,verbose_name=u'得分')
    confidence = models.FloatField(default=0.0,verbose_name=u'信心得分')
    news = models.ForeignKey(News, null=True,verbose_name=u'所属分享')
    time = models.DateTimeField(auto_now_add=True,verbose_name=u'评论时间')
    gold = models.IntegerField(default=0,verbose_name=u'赏金')
    words = models.TextField(null=True,verbose_name=u'评论')
    
    def __unicode__(self):
        return '1_%s' % self.id
    
    class Meta:
        ordering = ['-confidence',]
        verbose_name = u'回复1'
        verbose_name_plural = u'回复1'
        
class NewsComment2(models.Model):
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'发表用户')
    ups = models.IntegerField(default=0,verbose_name=u'顶')
    downs = models.IntegerField(default=0,verbose_name=u'沉')
    score = models.IntegerField(default=0,verbose_name=u'得分')
    confidence = models.FloatField(default=0.0,verbose_name=u'信心得分')
    newscomment1 = models.ForeignKey(NewsComment1, null=True,verbose_name=u'所属评论')
    time = models.DateTimeField(auto_now_add=True,verbose_name=u'评论时间')
    gold = models.IntegerField(default=0,verbose_name=u'赏金')
    words = models.TextField(null=True,verbose_name=u'评论')
    
    def __unicode__(self):
        return '2_%s' % self.id
    
    class Meta:
        ordering = ['-confidence',]
        verbose_name = u'回复2'
        verbose_name_plural = u'回复2'
      
class NewsComment3(models.Model):
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'发表用户')
    ups = models.IntegerField(default=0,verbose_name=u'顶')
    downs = models.IntegerField(default=0,verbose_name=u'沉')
    score = models.IntegerField(default=0,verbose_name=u'得分')
    confidence = models.FloatField(default=0.0,verbose_name=u'信心得分')
    newscomment2 = models.ForeignKey(NewsComment2, null=True,verbose_name=u'所属评论')
    time = models.DateTimeField(auto_now_add=True,verbose_name=u'评论时间')
    gold = models.IntegerField(default=0,verbose_name=u'赏金')
    words = models.TextField(null=True,verbose_name=u'评论')
    
    def __unicode__(self):
        return '3_%s' % self.id
    
    class Meta:
        ordering = ['-confidence',]
        verbose_name = u'回复3'
        verbose_name_plural = u'回复3'
        
class NewsComment4(models.Model):
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'发表用户')
    ups = models.IntegerField(default=0,verbose_name=u'顶')
    downs = models.IntegerField(default=0,verbose_name=u'沉')
    score = models.IntegerField(default=0,verbose_name=u'得分')
    confidence = models.FloatField(default=0.0,verbose_name=u'信心得分')
    newscomment3 = models.ForeignKey(NewsComment3, null=True,verbose_name=u'所属评论')
    time = models.DateTimeField(auto_now_add=True,verbose_name=u'评论时间')
    gold = models.IntegerField(default=0,verbose_name=u'赏金')
    words = models.TextField(null=True,verbose_name=u'评论')
    
    def __unicode__(self):
        return '4_%s' % self.id
    
    class Meta:
        ordering = ['-confidence',]
        verbose_name = u'回复4'
        verbose_name_plural = u'回复4'
   
class PartAdmin(models.Model):
    user = models.ForeignKey(MyUser, null=True,verbose_name=u'用户')
    newspart = models.ForeignKey(NewsPart, null=True,verbose_name=u'社群')
    
    def __unicode__(self):
        return '%s' % self.id
    
    class Meta:
        ordering = ['newspart',]
        verbose_name = u'社群管理员'
        verbose_name_plural = u'社群管理员'
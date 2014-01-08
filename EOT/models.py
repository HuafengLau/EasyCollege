#coding:utf-8

from django.db import models
from account.models import MyUser

class Eot_naming(models.Model):
    never_num = models.IntegerField(default=0,verbose_name=u'很少点名')
    sometimes_num = models.IntegerField(default=0,verbose_name=u'有时点名')
    often_num = models.IntegerField(default=0,verbose_name=u'经常点名')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'点名'
        verbose_name_plural = u'Eot_点名'
    
class Eot_naming_way(models.Model):
    no_num = models.IntegerField(default=0,verbose_name=u'不点名')
    sign_num = models.IntegerField(default=0,verbose_name=u'签到')
    answer_num = models.IntegerField(default=0,verbose_name=u'点名回答')
    hybrid_num = models.IntegerField(default=0,verbose_name=u'多种方式')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'点名方式'
        verbose_name_plural = u'Eot_点名方式'
    
class Eot_atmosphere(models.Model):
    dead_num = models.IntegerField(default=0,verbose_name=u'死气沉沉')
    normal_num = models.IntegerField(default=0,verbose_name=u'一般')
    active_num = models.IntegerField(default=0,verbose_name=u'较活跃')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'上课氛围'
        verbose_name_plural = u'Eot_上课氛围'
    
class Eot_teach_way(models.Model):
    PPT_num = models.IntegerField(default=0,verbose_name=u'PPT型')
    book_num = models.IntegerField(default=0,verbose_name=u'照本宣科型')
    teacher_num = models.IntegerField(default=0,verbose_name=u'自成一派型')
    hybrid_num = models.IntegerField(default=0,verbose_name=u'混合型')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'教学方式'
        verbose_name_plural = u'Eot_教学方式'
    
class Eot_popularity(models.Model):
    most_num = models.IntegerField(default=0,verbose_name=u'基本上人都去')
    more_num = models.IntegerField(default=0,verbose_name=u'大部分人去')
    less_num = models.IntegerField(default=0,verbose_name=u'少部分人去')
    nobody_num = models.IntegerField(default=0,verbose_name=u'基本没人去')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'上课人气'
        verbose_name_plural = u'Eot_上课人气'
    
class Eot_mid_test_way(models.Model):
    no_num = models.IntegerField(default=0,verbose_name=u'没有期中考')
    open_num = models.IntegerField(default=0,verbose_name=u'开卷考试')
    paper_num = models.IntegerField(default=0,verbose_name=u'闭卷考试')
    pravite_num = models.IntegerField(default=0,verbose_name=u'私下完成')
    inspect_num = models.IntegerField(default=0,verbose_name=u'其他考察方式')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'期中方式'
        verbose_name_plural = u'Eot_期中方式'
    
class Eot_final_test_way(models.Model):
    paper_num = models.IntegerField(default=0,verbose_name=u'闭卷考试')
    open_num = models.IntegerField(default=0,verbose_name=u'开卷考试')
    pravite_num = models.IntegerField(default=0,verbose_name=u'私下完成')
    inspect_num = models.IntegerField(default=0,verbose_name=u'其他考察方式')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'期末考方式'
        verbose_name_plural = u'Eot_期末考方式'
 
class Eot_final_test_degree(models.Model):
    hard_num = models.IntegerField(default=0,verbose_name=u'较难')
    soso_num = models.IntegerField(default=0,verbose_name=u'一般')
    easy_num = models.IntegerField(default=0,verbose_name=u'较容易')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'期末难度'
        verbose_name_plural = u'Eot_期末难度'
    
class Eot_reveal(models.Model):
    draw_importence_num = models.IntegerField(default=0,verbose_name=u'划重点')
    give_paper_num = models.IntegerField(default=0,verbose_name=u'给题目')
    nothing_num = models.IntegerField(default=0,verbose_name=u'什么也不给')
    others_num = models.IntegerField(default=0,verbose_name=u'其他泄题方式')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'透题'
        verbose_name_plural = u'Eot_透题'
    
class Eot_usual_work(models.Model):
    less_num = models.IntegerField(default=0,verbose_name=u'很少')
    some_num = models.IntegerField(default=0,verbose_name=u'有一些')
    more_num = models.IntegerField(default=0,verbose_name=u'很多')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'平时作业'
        verbose_name_plural = u'Eot_平时作业'
    
class Eot_mid_test(models.Model):
    yes_num = models.IntegerField(default=0,verbose_name=u'有期中考')
    no_num = models.IntegerField(default=0,verbose_name=u'没有期中考')
    
    def __unicode__(self):
        return self.id
    
    class Meta:        
        verbose_name = u'期中考'
        verbose_name_plural = u'Eot_期中考'
   
class Teacher(models.Model):
    university = models.CharField(max_length=30,null=True,verbose_name=u'学校')
    name = models.CharField(max_length=30,null=True,verbose_name=u'老师')
    value_num = models.IntegerField(default=0,null=True,verbose_name=u'评价人数')
    avg_score = models.FloatField(null=True, verbose_name=u'老师评分')
    
    def __unicode__(self):
        return '%s,%s' % (self.university, self.name)
    
    class Meta:
        ordering = ['university','name']
        verbose_name = u'评价老师'
        verbose_name_plural = u'评价老师'
    
class Eot(models.Model):
    course = models.CharField(max_length=30,null=True,verbose_name=u'课程名')
    teacher = models.CharField(max_length=30,null=True,verbose_name=u'任课老师')
    credit = models.FloatField(null=True, verbose_name=u'学分')
    #university_info_id = models.CharField(max_length=30,null=True,verbose_name=u'院校信息id')
    university = models.CharField(max_length=30,null=True,verbose_name=u'学校')
    college = models.CharField(max_length=30,null=True,verbose_name=u'学院')
    value_num = models.IntegerField(default=0,null=True,verbose_name=u'评价人数')
    course_avg_score = models.FloatField(verbose_name=u'课程评分')
    teacher_avg_score = models.FloatField(verbose_name=u'老师评分')
    history_avg_score = models.FloatField(null=True, verbose_name=u'历史平均分')
    like_num = models.IntegerField(default=0,verbose_name=u'好评')
    hate_num = models.IntegerField(default=0,verbose_name=u'差评')
    middle_num = models.IntegerField(default=0,verbose_name=u'中评')
    recommend_num = models.IntegerField(default=0,verbose_name=u'推荐')
    
    
    naming = models.ForeignKey(Eot_naming, null=True,verbose_name=u'点名')
    naming_way = models.ForeignKey(Eot_naming_way, null=True,verbose_name=u'点名方式')
    atmosphere = models.ForeignKey(Eot_atmosphere, null=True,verbose_name=u'气氛')
    teach_way = models.ForeignKey(Eot_teach_way, null=True,verbose_name=u'教学方式')
    popularity = models.ForeignKey(Eot_popularity, null=True,verbose_name=u'人气')
    
    mid_test = models.ForeignKey(Eot_mid_test, verbose_name=u'期中考试')
    mid_test_way = models.ForeignKey(Eot_mid_test_way, null=True,verbose_name=u'期中考方式')
    final_test_way = models.ForeignKey(Eot_final_test_way, null=True,verbose_name=u'期末考方式')
    final_test_degree = models.ForeignKey(Eot_final_test_degree, null=True,verbose_name=u'期末难度')
    reveal = models.ForeignKey(Eot_reveal, null=True,verbose_name=u'泄题')
    usual_work = models.ForeignKey(Eot_usual_work, null=True,verbose_name=u'平时作业')
    
    def __unicode__(self):
        return '%s,%s,%s' % (self.university, self.course, self.teacher)
    
    class Meta:
        ordering = ['university',]
        verbose_name = u'评课'
        verbose_name_plural = u'评课'
      
class Eot_data(models.Model):
    title = models.CharField(max_length=30,null=True,verbose_name=u'资料主题')
    description = models.CharField(max_length=100,null=True,verbose_name=u'资料说明')
    warning_num = models.IntegerField(default=0,null=True,verbose_name=u'资料举报')
    download_num =  models.IntegerField(default=0,null=True,verbose_name=u'下载次数')
    price_num =  models.IntegerField(default=0,verbose_name=u'资料定价')
    upload_time =  models.DateField(auto_now_add=True,verbose_name=u'上传时间')
    owner = models.ForeignKey(MyUser, verbose_name=u'资料拥有者')
    eot = models.ForeignKey(Eot, verbose_name=u'课程')
    file = models.FileField(upload_to='eot_data/', verbose_name=u'资料')
    profit = models.IntegerField(default=0,null=True,blank=True,verbose_name=u'资料收益')
    
class Eot_comment(models.Model):
    user = models.ForeignKey(MyUser, verbose_name=u'评论者')
    comment = models.TextField(verbose_name=u'评论内容')
    agree_num = models.IntegerField(default=0,verbose_name=u'评论赞')
    disagree_num = models.IntegerField(default=0,verbose_name=u'评论踩')
    eot = models.ForeignKey(Eot, verbose_name=u'课程', related_name='comment_set')
    time = models.DateField(auto_now_add=True, null=True,verbose_name=u'评论时间')
    
    def __unicode__(self):
        return '%s,%s' % (self.eot,self.user)
    
    class Meta:
        ordering = ['eot',]
        verbose_name = u'评教评论'
        verbose_name_plural = u'评教评论'
    
class First_3(models.Model):
    user = models.ForeignKey(MyUser, null=True, verbose_name=u'评论者')
    lucky = models.IntegerField(default=0,verbose_name=u'幸运儿') 
    eot = models.ForeignKey(Eot, null=True,verbose_name=u'课程')
    
    def __unicode__(self):
        return '%s,%s,%s' % (self.eot, self.lucky, self.user)
    
    class Meta:
        ordering = ['eot','lucky']
        verbose_name = u'评教评论者'
        verbose_name_plural = u'评教评论者'

class Eotdata_comment(models.Model):
    user = models.ForeignKey(MyUser, verbose_name=u'评论者')
    comment = models.TextField(verbose_name=u'评论内容')
    eot_data = models.ForeignKey(Eot_data, verbose_name=u'课程资料')
    time = models.DateField(auto_now_add=True, null=True,verbose_name=u'评论时间')
    
    def __unicode__(self):
        return '%s,%s' % (self.eot_data,self.user)
    
    class Meta:
        ordering = ['eot_data',]
        verbose_name = u'资料评论'
        verbose_name_plural = u'资料评论'
    
class Eot_img(models.Model):
    eot = models.ForeignKey(Eot, blank=True,null=True,on_delete=models.SET_NULL,
        related_name='eot_toImg',verbose_name=u'课程')
    img = models.ImageField(upload_to='eot_img/',blank=True,null=True)
    owner = models.ForeignKey(MyUser, null=True,blank=True,
        on_delete=models.SET_NULL,related_name='owner_toImg', verbose_name=u'图片上传者')
    like_num = models.IntegerField(default=0,blank=True,null=True,verbose_name=u'图片赞')
    title = models.CharField(max_length=30,blank=True,null=True,verbose_name=u'资料主题')
    description = models.CharField(max_length=50,blank=True,null=True,verbose_name=u'资料说明')
    upload_time =  models.DateField(auto_now_add=True,verbose_name=u'上传时间')
    if_safe = models.CharField(max_length=3,blank=True,null=True,verbose_name=u'图片安全')
    

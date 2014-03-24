#coding:utf-8

from django.contrib import admin
from News.models import News,NewsPart,NewsPartRule,NewsComment1,NewsComment2,NewsComment3,NewsComment4,PartAdmin,NewsPic


class NewsAdmin(admin.ModelAdmin):
    """docstring for NewsAdmin"""
    list_display = ('user', 'time','type','title', 'newspart','ups','downs','gold','score','controversy','hot')
    list_filter = ('user', 'type')
    #ordering = ('user', )

class NewsPicAdmin(admin.ModelAdmin):
    """docstring for NewsPicAdmin"""
    list_display = ('pic', 'news')
    list_filter = ('news',)
    ordering = ('news', )
    
class NewsPartAdmin(admin.ModelAdmin):
    """docstring for NewsPartAdmin"""
    list_display = ('part', 'realPart','num','user_num','can_link','can_text','can_pic','can_mp3','time')
    #list_filter = ('part', 'type')
    ordering = ('part', )
 
class NewsPartRuleAdmin(admin.ModelAdmin):
    """docstring for NewsPartAdmin"""
    list_display = ('newspart', 'rule')
    list_filter = ('newspart', )
    ordering = ('newspart', )
 
class NewsComment1Admin(admin.ModelAdmin):
    """docstring for NewsComment1Admin"""
    list_display = ('news','user','ups', 'downs','score','confidence','time','gold')
    list_filter = ('news', )
    ordering = ('-confidence', )
    
class NewsComment2Admin(admin.ModelAdmin):
    """docstring for NewsComment2Admin"""
    list_display = ('newscomment1','user','ups', 'downs','score','confidence','time','gold')
    list_filter = ('newscomment1', )
    ordering = ('-confidence', )
  
class NewsComment3Admin(admin.ModelAdmin):
    """docstring for NewsComment3Admin"""
    list_display = ('newscomment2','user','ups', 'downs','score','confidence','time','gold')
    list_filter = ('newscomment2', )
    ordering = ('-confidence', )
  
class NewsComment4Admin(admin.ModelAdmin):
    """docstring for NewsComment4Admin"""
    list_display = ('newscomment3','user','ups', 'downs','score','confidence','time','gold')
    list_filter = ('newscomment3', )
    ordering = ('-confidence', )

class PartAdminAdmin(admin.ModelAdmin):
    """docstring for PartAdminAdmin"""
    list_display = ('newspart','user')
    list_filter = ('newspart', )
    ordering = ('newspart', )
 
admin.site.register(News, NewsAdmin)
admin.site.register(NewsPart, NewsPartAdmin)
admin.site.register(NewsPartRule, NewsPartRuleAdmin)
admin.site.register(NewsComment1, NewsComment1Admin)
admin.site.register(NewsComment2, NewsComment2Admin)
admin.site.register(NewsComment3, NewsComment3Admin)
admin.site.register(NewsComment4, NewsComment4Admin)
admin.site.register(PartAdmin, PartAdminAdmin)
admin.site.register(NewsPic, NewsPicAdmin)
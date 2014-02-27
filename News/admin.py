#coding:utf-8

from django.contrib import admin
from News.models import News,NewsPart


class NewsAdmin(admin.ModelAdmin):
    """docstring for NewsAdmin"""
    list_display = ('user', 'time','type','title', 'part','ups','downs','gold','score','controversy','hot')
    list_filter = ('user', 'type')
    #ordering = ('user', )

class NewsPartAdmin(admin.ModelAdmin):
    """docstring for NewsPartAdmin"""
    list_display = ('part', 'realPart','num')
    #list_filter = ('part', 'type')
    ordering = ('part', )
    
admin.site.register(News, NewsAdmin)
admin.site.register(NewsPart, NewsPartAdmin)
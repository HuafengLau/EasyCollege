#coding:utf-8

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import MyUser
from Index.models import Avatar,Feeds_news,Feeds_comment,Feeds_followNews,Folder,Collect,WatchFolder

        
class AvatarAdmin(admin.ModelAdmin):
    """docstring for TeacherAdmin"""
    list_display = ('photo','user')
    list_filter = ('user',)
    ordering = ('user',)
    
class Feeds_followNewsAdmin(admin.ModelAdmin):
    """docstring for Feeds_followNewsAdmin"""
    list_display = ('type','owner','creator','time')
    list_filter = ('owner','owner','creator')
    ordering = ('time','owner')
    
class Feeds_newsAdmin(admin.ModelAdmin):
    """docstring for Feeds_newsAdmin"""
    list_display = ('type','owner','creator','time','gold_num')
    list_filter = ('owner','owner','creator')
    ordering = ('time','owner')

class Feeds_commentAdmin(admin.ModelAdmin):
    """docstring for Feeds_commentAdmin"""
    list_display = ('type','owner','creator','time','gold_num')
    list_filter = ('owner','owner','creator')
    ordering = ('time','owner')
    

    
admin.site.register(Avatar, AvatarAdmin)
admin.site.register(Feeds_followNews, Feeds_followNewsAdmin)
admin.site.register(Feeds_news, Feeds_newsAdmin)
admin.site.register(Feeds_comment, Feeds_commentAdmin)
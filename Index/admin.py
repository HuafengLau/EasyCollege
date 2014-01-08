#coding:utf-8

from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import MyUser
from Index.models import Avatar

        
class AvatarAdmin(admin.ModelAdmin):
    """docstring for TeacherAdmin"""
    list_display = ('photo','user')
    list_filter = ('user',)
    ordering = ('user',)
    
admin.site.register(Avatar, AvatarAdmin)
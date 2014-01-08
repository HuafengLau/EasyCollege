#coding:utf-8

from django.contrib import admin
from Center.models import User_info


class User_infoAdmin(admin.ModelAdmin): 
    """docstring for User_infoAdmin"""
    list_display = ('user','store_eot','download_Eotdata','nocomment_Eotdata')    
    list_filter = ('user',)
    ording = ('user',)
 
admin.site.register(User_info, User_infoAdmin) 
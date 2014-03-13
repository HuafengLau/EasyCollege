#coding:utf-8

from django.contrib import admin
from Center.models import User_info,Honour


class User_infoAdmin(admin.ModelAdmin): 
    """docstring for User_infoAdmin"""
    list_display = ('user','store_eot','download_Eotdata','nocomment_Eotdata','grade','subscription')    
    list_filter = ('user',)
    ording = ('user',)
    
class HonourAdmin(admin.ModelAdmin): 
    """docstring for HonourAdmin"""
    list_display = ('user','img','info')    
    list_filter = ('user','img')
    ording = ('user',)
 
admin.site.register(User_info, User_infoAdmin) 
admin.site.register(Honour, HonourAdmin) 
#coding:utf-8

from django.contrib import admin
from University.models import University_info

class University_infoAdmin(admin.ModelAdmin):
    """docstring for University_infoAdmin"""
    list_display = ('school', 'college', 'major','id')
    ordering = ('school','college', 'major')
    

    
admin.site.register(University_info, University_infoAdmin)

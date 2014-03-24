#coding:utf-8

from django.contrib import admin
#from Business.models import Credit, Major_course
from Business.models import AuthorLog

class AuthorLogAdmin(admin.ModelAdmin):
    """docstring for AuthorLogAdmin"""
    list_display = ('user', 'type', 'openid')
    list_filter = ('type',)
    ordering = ('type','user' )


'''
class CreditAdmin(admin.ModelAdmin):
    """docstring for CreditAdmin"""
    list_display = ('user', 'university_info_id', 'course_name', 'add_money')
    list_filter = ('user', 'grade')
    ordering = ('user', )
    
class Major_courseAdmin(admin.ModelAdmin):
    """docstring for CreditAdmin"""
    list_display = ('major_id', 'course')
    list_filter = ('major_id',)
    ording = ('major_name',)'''

    
admin.site.register(AuthorLog, AuthorLogAdmin)
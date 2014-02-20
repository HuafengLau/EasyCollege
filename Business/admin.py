#coding:utf-8

from django.contrib import admin
from Business.models import Credit, Major_course


class CreditAdmin(admin.ModelAdmin):
    """docstring for CreditAdmin"""
    list_display = ('user', 'university_info_id', 'course_name', 'add_money')
    list_filter = ('user', 'grade')
    ordering = ('user', )
    
class Major_courseAdmin(admin.ModelAdmin):
    """docstring for CreditAdmin"""
    list_display = ('major_id', 'course')
    list_filter = ('major_id',)
    ording = ('major_name',)


admin.site.register(Credit, CreditAdmin)
admin.site.register(Major_course, Major_courseAdmin)
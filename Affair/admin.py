#coding:utf-8

from django.contrib import admin
from Affair.models import *

class Report_eotDataAdmin(admin.ModelAdmin): 
    """docstring for Report_eotDataAdmin"""
    list_display = ('result','report_time', 'reporter','suspect')
    list_filter = ('result',)
    ording = ('result','report_time',) 
 
admin.site.register(Report_eotData, Report_eotDataAdmin) 


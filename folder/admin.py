#coding:utf-8

from django.contrib import admin
from Index.models import Folder,Collect,WatchFolder


class FolderAdmin(admin.ModelAdmin):
    """docstring for FolderAdmin"""
    list_display = ('owner', 'name')
    list_filter = ('owner', )
    ordering = ('owner', )

class CollectAdmin(admin.ModelAdmin):
    """docstring for CollectAdmin"""
    list_display = ('folder', 'news')
    list_filter = ('folder', )
    ordering = ('folder', )    
    
class WatchFolderAdmin(admin.ModelAdmin):
    """docstring for WatchFolderAdmin"""
    list_display = ('user', 'folder')
    list_filter = ('folder', 'user')
    ordering = ('user', )       
    
admin.site.register(Folder, FolderAdmin)
admin.site.register(Collect, CollectAdmin)
admin.site.register(WatchFolder,WatchFolderAdmin)

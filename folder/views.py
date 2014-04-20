#coding:utf-8

from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from Index.form import AvatarForm,FolderForm
from django.conf import settings
from account.models import MyUser
from Index.models import Folder,Collect,WatchFolder
from News.models import News


def folder(request):
    folderHTML = True
    user = request.user
    folderform = FolderForm()
    if user.is_authenticated():   
        watchFolders = WatchFolder.objects.filter(user=user)
        if watchFolders:
            id_list = []
            for watchFolder in watchFolders:
                id_list.append(watchFolder.folder.id)
                folders = Folder.objects.all().exclude(owner=user).exclude(id__in=id_list)
        else:
             folders = Folder.objects.all().exclude(owner=user)
    else:
        folders = Folder.objects.all()
    if folders:
        sorted_folders = sorted(list(folders), key=lambda x: WatchFolder.objects.filter(folder=x).count(),reverse = True)
    else:
        sorted_folders = None
    
    return render_to_response('folder.html', locals(),
        context_instance=RequestContext(request))
 
@login_required
@csrf_exempt
def newBuild(request):
    if request.is_ajax():
        if request.method == 'POST':
            try:
                new_folder = Folder(
                    name = request.POST.get('name'),
                    description = request.POST.get('desc'),
                    owner = request.user
                )
                new_folder.save()
                if request.POST.get('news_id'):
                    this_news = News.objects.get(id=request.POST.get('news_id'))
                    new_collect = Collect(
                        folder = new_folder,
                        news = this_news
                    )
                    new_collect.save()
                    this_news.collectNum += 1
                    this_news.save()
                    response = HttpResponse('buildAndCollect')
                    return response
                else:
                    response = HttpResponse('build')
                    return response
            except:
                response = HttpResponse('wrong')
                return response
    else:
        if request.method == 'POST':
            form = FolderForm(request.POST)
            if form.is_valid():
                new_folder = Folder(
                    name = form.cleaned_data['name'],
                    description = form.cleaned_data['description'],
                    owner = request.user
                )
                new_folder.save()
                return HttpResponseRedirect('/folder/')
            else:
                return render_to_response('folder.html', locals(),
                    context_instance=RequestContext(request))

@login_required
@csrf_exempt
def collect(request):
    if request.is_ajax():
        if request.method == 'POST':
            try:
                this_news = News.objects.get(id=request.POST.get('news_id'))
                this_folder = Folder.objects.get(id=request.POST.get('folder_id'))
                new_collect = Collect(
                    folder = this_folder,
                    news = this_news
                )
                new_collect.save()
                this_news.collectNum += 1
                this_news.save()
                response = HttpResponse('collect')
                return response
            except:
                response = HttpResponse('wrong')
                return response

@csrf_exempt
@login_required                
def watch(request):
   if request.is_ajax() and request.method == 'POST':
       try:
           id = request.POST.get('folder_id')
           folder = Folder.objects.get(id=id)
           new_watchFolder = WatchFolder(
               folder = folder,
               user = request.user
           )
           new_watchFolder.save()
           response = HttpResponse('watch')
           return response
       except:
           response = HttpResponse('wrong')
           return response
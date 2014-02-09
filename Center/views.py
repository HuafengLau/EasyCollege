#coding:utf-8

from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from EOT.models import Eot_data, Eot
from Center.models import User_info

@login_required(login_url='/log/')
def center(request):
    user = request.user
    my_Eotdata = Eot_data.objects.filter(owner=user)
        
    if not my_Eotdata:
        my_Eotdata = None
    else:
        my_Eotdata_after_range_num = 5        
        my_Eotdata_befor_range_num = 4       
        try:                     
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(my_Eotdata,6)   
        try:                     
            my_Eotdata_list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            my_Eotdata_list = paginator.page(paginator.num_pages)
        if page >= my_Eotdata_after_range_num:
            my_Eotdata_page_range = paginator.page_range[page-my_Eotdata_after_range_num:page+my_Eotdata_befor_range_num]
        else:
            my_Eotdata_page_range = paginator.page_range[0:int(page)+my_Eotdata_befor_range_num]
        my_Eotdata = my_Eotdata_list
    
    try: 
        this_user_info = User_info.objects.get(user=user)
    except:       
        this_user_info = User_info(
            store_eot = '',
            user = user,
            download_Eotdata = '',
            nocomment_Eotdata = '',
            grade = u'公民'
        )
        this_user_info.save()
         
    if this_user_info.store_eot:
        storeEot_list = this_user_info.store_eot.split(';')[:-1]
        my_storeEot = Eot.objects.filter(id__in=storeEot_list)
        my_storeEot_after_range_num = 5        
        my_storeEot_befor_range_num = 4       
        try:                     
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(my_storeEot,6)   
        try:                     
            my_storeEot_list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            my_storeEot_list = paginator.page(paginator.num_pages)
        if page >= my_storeEot_after_range_num:
            my_storeEot_page_range = paginator.page_range[page-my_storeEot_after_range_num:page+my_storeEot_befor_range_num]
        else:
            my_storeEot_page_range = paginator.page_range[0:int(page)+my_storeEot_befor_range_num]
        my_storeEot = my_storeEot_list
        
    else:
        my_storeEot = None
        
    if this_user_info.download_Eotdata:
        download_list = this_user_info.download_Eotdata.split(';')[:-1]
        download_Eotdata = Eot_data.objects.filter(id__in=download_list)
        
        download_Eotdata_after_range_num = 5        
        download_Eotdata_befor_range_num = 4       
        try:                     
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(download_Eotdata,6)   
        try:                     
            download_Eotdata_list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            download_Eotdata_list = paginator.page(paginator.num_pages)
        if page >= download_Eotdata_after_range_num:
            download_Eotdata_page_range = paginator.page_range[page-download_Eotdata_after_range_num:page+download_Eotdata_befor_range_num]
        else:
            download_Eotdata_page_range = paginator.page_range[0:int(page)+download_Eotdata_befor_range_num]
        download_Eotdata = download_Eotdata_list
    else:
        download_Eotdata = None
        
    centerHTML = True
    return render_to_response('center.html',locals(),
        context_instance=RequestContext(request))
        
def delStore(request, eot_id):
    user = request.user
    this_user_info = User_info.objects.get(user=user)
    storeEot_list = this_user_info.store_eot.split(';')[:-1]
    storeEot_list.remove('%s' % eot_id)
    if storeEot_list:
        s = ';'.join(storeEot_list)
        this_user_info.store_eot = s + ';'
    else:
        this_user_info.store_eot = ''
    this_user_info.save()
    return HttpResponseRedirect('/center/')
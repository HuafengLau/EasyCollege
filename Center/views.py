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
from Index.form import AvatarForm
from Index.models import Avatar

@csrf_exempt
@login_required(login_url='/log/')
def center(request):
    if request.is_ajax():
        if request.method == 'GET':
            if 'nic_name' in request.GET:
                user = request.user
                user.nic_name = request.GET.get('nic_name')
                user.save()
                response = HttpResponse(u'更改昵称成功！')
                return response
            if 'sign' in request.GET:
                if len(request.GET.get('sign')) > 50:
                    response = HttpResponse(u'个性签名不能超过50个字哦！')
                    return response
                else:
                    user = request.user
                    this_user_info = User_info.objects.get(user=user)
                    this_user_info.sign = request.GET.get('sign')
                    this_user_info.save()
                    response = HttpResponse(u'更改成功！')
                    return response
            if 'whenNewsbeGold' in request.GET:
                if len(request.GET.get('whenNewsbeGold')) > 20:
                    response = HttpResponse(u'自动回复不能超过20个字哦！')
                    return response
                else:
                    user = request.user
                    this_user_info = User_info.objects.get(user=user)
                    this_user_info.when_newsbeGold = request.GET.get('whenNewsbeGold')
                    this_user_info.save()
                    response = HttpResponse(u'更改成功！')
                    return response
            if 'whenCommentbeGold' in request.GET:
                if len(request.GET.get('whenCommentbeGold')) > 20:
                    response = HttpResponse(u'自动回复不能超过20个字哦！')
                    return response
                else:
                    user = request.user
                    this_user_info = User_info.objects.get(user=user)
                    this_user_info.when_commentbeGold = request.GET.get('whenCommentbeGold')
                    this_user_info.save()
                    response = HttpResponse(u'更改成功！')
                    return response
            if 'beWatched' in request.GET:
                if len(request.GET.get('beWatched')) > 20:
                    response = HttpResponse(u'自动回复不能超过20个字哦！')
                    return response
                else:
                    user = request.user
                    this_user_info = User_info.objects.get(user=user)
                    this_user_info.when_beWatched = request.GET.get('beWatched')
                    this_user_info.save()
                    response = HttpResponse(u'更改成功！')
                    return response
        if request.method == 'POST':
            if 'change' in request.POST:
                user = request.user
                if request.POST.get('change') == 'show_email':
                    this_user_info = User_info.objects.get(user=user)
                    if this_user_info.show_email:
                        this_user_info.show_email = False
                        this_user_info.save()
                    else:
                        this_user_info.show_email = True
                        this_user_info.save()
                    response = HttpResponse()
                    return response
                
    else:
        user = request.user
        form = AvatarForm()
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
                user = new_user,
                download_Eotdata = '',
                nocomment_Eotdata = '',
                grade = u'公民',
                subscription = 'ExplainCY;Funny;Home-news;Life;AskAnything;',
                beWatched = '',
                watching = '',
                upVoted_news = '',
                downVoted_news = '',
                upVoted_comment1 = '',
                upVoted_comment2 = '',
                upVoted_comment3 = '',
                upVoted_comment4 = '',
                downVoted_comment1 = '',
                downVoted_comment2 = '',
                downVoted_comment3 = '',
                downVoted_comment4 = '',
                when_newsbeGold = u'你的支持是我分享的动力：）',
                when_commentbeGold = u'下一次，我的评论将更有含金量：）',
                when_beWatched = u'感谢关注：）',
                agree_num = 0
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

@csrf_exempt 
@login_required(login_url='/log/')    
def upload_avatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                old_avatar = Avatar.objects.get(user = request.user)
                old_avatar.delete()
                old_file = settings.MEDIA_ROOT + '/' + str(old_avatar.photo)
                if os.path.isfile(old_file):
                    os.remove(old_file)
                
            except:
                pass
            info = Avatar(
                photo = form.cleaned_data['photo'],
                user = request.user
            )
            info.save()
            name = str(info.photo).split('/')[1]
            user = request.user
            user.avatar = 'avatar/%s' % name
            user.save()
        return HttpResponseRedirect('/center/#set_avatar')
            
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
#coding:utf-8
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.conf import settings
from News.models import NewsPart,News,NewsPic,NewsComment1,NewsComment2,NewsComment3,NewsComment4
from News.form import LinkNewsForm, TextNewsForm, PicNewsForm, mp3NewsForm
import datetime
import calendar
from Center.models import User_info
from math import sqrt, log10, log
import pytz
import json, os, time
from account.models import MyUser
from Index.models import Feeds_news,Feeds_comment,Feeds_followNews

from django.core.urlresolvers import reverse
from django.views import generic
from django.views.decorators.http import require_POST
from jfu.http import upload_receive, UploadResponse, JFUResponse

import traceback

def score(ups,downs):
    return ups - downs

# 当前为10倍票可保持原位
def hot(ups, downs, read, time):
    s = score(ups, downs)
    order = log10(max(abs(s), 1))
    read_score = log(max(read, 1),500)
    if s > 0:
        sign = 1
    elif s < 0:
        sign = -1
    else:
        sign = 0
    seconds = (time-datetime.datetime(2014,2,11,10,46,0,0,pytz.utc)).total_seconds()
    return round(sign * order + read_score + seconds / (24*3600), 7)

def controversy(ups, downs):
    return float(ups + downs) / max(abs(score(ups, downs)), 1)
    
def confidence(ups, downs):
    n = ups + downs

    if n == 0:
        return 0

    z = 1.281551565545 # 80% confidence
    p = float(ups) / n

    left = p + 1/(2*n)*z*z
    right = z*sqrt(p*(1-p)/n + z*z/(4*n*n))
    under = 1+1/n*z*z

    return (left - right) / under

def readNews(request):
    if request.is_ajax() and request.method == 'GET':
        this_id = request.GET.get('id')
        this_news = News.objects.get(id=this_id)
        read = this_news.read + 1
        ups = this_news.ups
        downs = this_news.downs
        this_news.read = read
        this_news.hot = hot(ups, downs, read, this_news.time)
        this_news.save()
        resposne = HttpReponse('yes')
        return resposne
    else:
        response = HttpResponse('wrong')
        return resposne
    
@login_required(login_url='/log/') 
def mySubscription(request):
    if request.is_ajax() and request.method == 'GET':
        user = request.user
        this_user_info = User_info.objects.get(user=user)
        if 'part' in request.GET:
            part = request.GET.get('part')
            this_part = NewsPart.objects.get(part=part)
            if part in this_user_info.subscription:
                this_user_info.subscription = this_user_info.subscription.replace('%s;' % part, '')
                this_user_info.save()
                this_part.user_num -= 1
                this_part.save()
                reponse = HttpResponse(u'已取消订阅：）')
                return reponse
            else:
                this_user_info.subscription += '%s;' % part
                this_user_info.save()
                this_part.user_num += 1
                this_part.save()
                reponse = HttpResponse(u'订阅成功：）')
                return reponse
        if 'order' in request.GET:
            order = request.GET.get('order')
            subscriptions = this_user_info.subscription.split(';')[:-1]
            notSubs = NewsPart.objects.all().exclude(part__in=subscriptions).order_by(order)
            return render_to_response('subscriptionOrder.html',locals(),
                context_instance=RequestContext(request))
        else:
            return render_to_response('404.html',locals(),
                context_instance=RequestContext(request)) 
    elif request.method == 'GET':
        newsHTML = True
        user = request.user
        this_user_info = User_info.objects.get(user=user)
        subscriptions = this_user_info.subscription.split(';')[:-1]
        allParts = NewsPart.objects.all()
        mySubs = allParts.filter(part__in=subscriptions).order_by('part')
        notSubs = allParts.exclude(part__in=subscriptions).order_by('part')
        top_newsParts = allParts.order_by('-num','-user_num','part')[:19]
        
        return render_to_response('mySubscription.html',locals(),
                context_instance=RequestContext(request))
    else:
        return render_to_response('404.html',locals(),
            context_instance=RequestContext(request)) 
    
def news(request):
    return HttpResponseRedirect('/news/All/hot/')

@login_required(login_url='/log/') 
@csrf_exempt
def uploadFile(request,this_type,this_id):
    if request.method == 'GET':
        type  = this_type
        id = this_id
        this_news = News.objects.get(id=id)
        return render_to_response('forUpload.html',locals(),
            context_instance=RequestContext(request)) 
    
@login_required(login_url='/log/')     
def finishUpload(request,this_id):
    this_news = News.objects.get(id=this_id)
    if this_news.type == 'pic':
        newspics = NewsPic.objects.filter(news=this_news)
        if not newspics:
            feeds = Feeds_followNews.objects.filter(news = this_news)
            if feeds:
                for feed in feeds:
                    feed.owner.message -= 1
                    feed.owner.save()
            this_news.delete()
            return HttpResponseRedirect('/news/All/hot/')
        else:
            url = '/news/%s/hot/showNews/%s/' % (this_news.newspart.part,this_news.id)
            return HttpResponseRedirect(url)
    elif this_news.type == 'mp3':
        try:
            mp3 = this_news.mp3
            if not mp3:
                feeds = Feeds_followNews.objects.filter(news = this_news)
                if feeds:
                    for feed in feeds:
                        feed.owner.message -= 1
                        feed.owner.save()
                this_news.delete()
                return HttpResponseRedirect('/news/All/hot/')
            url = '/news/%s/hot/showNews/%s/' % (this_news.newspart.part,this_news.id)
            return HttpResponseRedirect(url)
        except:
            this_news.delete()
            return HttpResponseRedirect('/news/All/hot/')
    else:
        return render_to_response('404.html',locals(),
            context_instance=RequestContext(request))

@login_required(login_url='/log/')     
def giveupUpload(request,this_id):
    this_news = News.objects.get(id=this_id)
    feeds = Feeds_followNews.objects.filter(news = this_news)
    if feeds:
        for feed in feeds:
            feed.owner.message -= 1
            feed.owner.save()
    if this_news.type == 'pic':       
        newspics = NewsPic.objects.filter(news=this_news)
        if newspics:
            for newspic in newspics:
                try:
                    os.unlink( newspic.pic.path )
                except:
                    pass
                newspic.delete()
        this_news.delete()
        return HttpResponseRedirect('/news/All/hot/')
    elif this_news.type == 'mp3':
        os.unlink( this_news.mp3.path )   
        this_news.delete()
        return HttpResponseRedirect('/news/All/hot/')
    else:
        return render_to_response('404.html',locals(),
            context_instance=RequestContext(request))            
    
@login_required(login_url='/log/') 
@require_POST
def upload( request ):   
    type = request.POST.get('type')
    id = request.POST.get('id')
    file = upload_receive( request )
    this_news = News.objects.get(id=id)
    if type == 'pic':
        instance = NewsPic( 
            pic = file,
            news = this_news
        )
        instance.save()
        basename = os.path.basename( instance.pic.path )
    elif type == 'mp3':
        this_news.mp3 = file
        this_news.save()
        instance = this_news
        basename = os.path.basename( instance.mp3.path )
    else:
        pass
    file_dict = {
        'name' : basename,
        'size' : file.size,
        'url': settings.MEDIA_URL + 'news_pic/'+ basename,
        'thumbnailUrl': settings.MEDIA_URL + 'news_pic/'+ basename,
        'deleteUrl': reverse('jfu_delete', kwargs = { 'pk': instance.pk }),
        'deleteType': 'POST',
    }

    return UploadResponse( request, file_dict )    

        
@login_required(login_url='/log/')   
@require_POST
def upload_delete( request, pk ):
    success = True
    type = request.POST.get('type')
    id = request.POST.get('id')
    if type == 'pic':
        try:
            instance = NewsPic.objects.get( pk = pk )
            os.unlink( instance.pic.path )
            instance.delete()            
        except NewsPic.DoesNotExist:
            success = False
    elif type == 'mp3':
        try:
            instance = News.objects.get( pk = pk )   
            os.unlink( instance.mp3.path )   
            instance.mp3 = None
            instance.save()
        except NewsPic.DoesNotExist:
            success = False
    else:
        success = False
    return JFUResponse( request, success )
    
@login_required(login_url='/log/') 
def newsVote(request):
    if request.is_ajax() and request.method == 'GET':
        if 'news_id' in request.GET:
            news_id = request.GET.get('news_id')
            vote = request.GET.get('vote')
            this_news = News.objects.get(id=news_id)
            user = request.user
            this_user_info = User_info.objects.get(user=user)
            ups = this_news.ups
            downs = this_news.downs
            if vote == '1':   
                if news_id in this_user_info.upVoted_news:
                    response = HttpResponse('wrong')
                    return response
                else:
                    this_news.user.agree_num += 1
                    this_news.user.save()
                    ups += 1
                    this_user_info.upVoted_news += '%s;' % news_id
                    this_user_info.save()
                    this_feed = Feeds_news(
                        type = 'newsVoteUp',
                        showText = True,
                        owner = this_news.user,
                        creator = user,
                        news = this_news,
                        gold_num = 0,
                    )
                    this_feed.save()
                    this_feed.owner.message += 1
                    this_feed.owner.save()
                    this_news.agree_man += '%s;' % user.id
            elif vote == '0':
                downs += 1
                if news_id in this_user_info.downVoted_news:
                    response = HttpResponse('wrong')
                    return response
                else:
                    this_user_info.downVoted_news += '%s;' % news_id
                    this_user_info.save()
            else:
                response = HttpResponse('wrong')
                return response
            
            now = datetime.datetime.now(pytz.utc)

            if (now - this_news.time).total_seconds() < 43200.0:
                user.money += 3
                user.save()
            
            read = this_news.read
            this_news.ups = ups
            this_news.downs = downs
            this_news.score = ups-downs
            this_news.hot = hot(ups, downs, read, this_news.time)
            this_news.controversy = controversy(ups, downs)
            this_news.save()
            
            return render_to_response('afterVote.html',locals(),
                context_instance=RequestContext(request))
    
def which_news(request,news_part,small_part):
    user = request.user   
    newsHTML = True
    newsBase = True
    allNewsPart = NewsPart.objects.all()
    part = allNewsPart.get(part=news_part)
    smallPart = small_part
    SimilarHtml = 'Similar' + news_part + '.html'
    smallParts = [u'热门',u'最新',u'热议',u'得分',u'镀金']
   
    newsParts = allNewsPart.filter(open=True,secret=False).order_by('-num','-user_num','part')
    
    top_newsParts = newsParts.exclude(part__in=['All','MySubs'])
    #more_newsParts = newsParts[25:]
    if user.is_authenticated():
        this_user_info = User_info.objects.get(user=user)
        subscriptions = this_user_info.subscription.split(';')[:-1]
        mySubs = allNewsPart.filter(part__in=subscriptions).order_by('part')
        otherParts = allNewsPart.exclude(part__in=subscriptions).order_by('part')
    else:
        defaultList = ['Funny','Life','Music','Home-news','ReportCY','Gossip']
        mySubs = allNewsPart.filter(part__in=defaultList).order_by('part')
        otherParts = allNewsPart.exclude(part__in=defaultList).order_by('part')
    
    if news_part == 'All':
        newses = News.objects.filter(open=True,secret=False)
    elif news_part == 'MySubs':
        newses = News.objects.filter(newspart__in=mySubs)
    else:
        newses = News.objects.filter(newspart=part)
        
        
    def cut(arr, indices):  
        return [arr[i:j] for i, j in zip([0]+indices, indices+[None])]  
                
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day
    _weekday,_lastday = calendar.monthrange(year,month)  
    _sundays = [x for x in range(6-_weekday+1,_lastday+1,7)]  

    weekList =  cut(range(1,_lastday+1),_sundays)

    for index, item in enumerate(weekList):
        if day in item:
            this_week = item
            break

    start_date = datetime.datetime(year,month,this_week[0],0,0,0,0)+ datetime.timedelta(days=-1)
    end_date = datetime.datetime.today()+ datetime.timedelta(days=1)
    weekTopList = newses.filter(time__range=(start_date, end_date)).order_by('-score','-time')[:8]
        
    hot_newses = newses.order_by('-hot','-time')[:25]
    gilded_newses = newses.order_by('-gold','-time')[:30]
    controversial_newses = newses.order_by('-controversy','-time')[:25]
    
    #top_newses = newses.order_by('-score','-time')[:5]
    new_newses = newses.order_by('-time')[:20]
    now = datetime.datetime.now(pytz.utc)
    new_newslist = []

    for news in new_newses: 
        if (now - news.time).total_seconds() < 43200.0:
            new_newslist.append(news)
    
    Comment1 = NewsComment1.objects.all()
    Comment2 = NewsComment2.objects.all()
    comments = sorted(list(Comment1) + list(Comment2), key=lambda x: x.time,reverse = True)
    newComments = comments[:6]
    
    return render_to_response('newsBase.html',locals(),
        context_instance=RequestContext(request))
            
@login_required(login_url='/log/')         
def submit_news(request,news_part, news_type):
    user = request.user
    newsHTML = True
    this_user_info = User_info.objects.get(user=user)
    subscriptions = this_user_info.subscription.split(';')[:-1]
    mySubs = NewsPart.objects.filter(part__in=subscriptions).order_by('part')
    part = NewsPart.objects.get(part=news_part)
    part_All = NewsPart.objects.get(part='All')
    RuleHtml = 'Rule'+ news_part + '.html'
    SimilarHtml = 'Similar' + news_part + '.html'
    AdminHtml = 'Admin' + news_part + '.html'
    type = news_type
    top_newsParts = NewsPart.objects.all().order_by('-num','-user_num','part')[:19]
 
    if request.method == 'GET':
        if news_part == 'All' or news_part == 'MySubs':
            linkForm = LinkNewsForm()
            textForm = TextNewsForm()
            picForm = PicNewsForm()
            mp3Form = mp3NewsForm()
        else:
            line = '--------请选择--------'
            class this_LinkNewsForm(LinkNewsForm):
                def __init__(self, *args, **kwargs):  
                    super(this_LinkNewsForm, self).__init__(*args, **kwargs)  
                    self.fields['newspart'].choices = [('', line)] + [
                        (part.id, '%s / %s' % (part.part,part.realPart)) ]
            
            class this_PicNewsForm(PicNewsForm):
                def __init__(self, *args, **kwargs):  
                    super(this_PicNewsForm, self).__init__(*args, **kwargs)  
                    self.fields['newspart'].choices = [('', line)] + [
                        (part.id, '%s / %s' % (part.part,part.realPart)) ]
                    
            class this_TextNewsForm(TextNewsForm):
                def __init__(self, *args, **kwargs):  
                    super(this_TextNewsForm, self).__init__(*args, **kwargs)  
                    self.fields['newspart'].choices = [('', line)] + [
                        (part.id, '%s / %s' % (part.part,part.realPart)) ]
            
            class this_mp3NewsForm(mp3NewsForm):
                def __init__(self, *args, **kwargs):  
                    super(this_mp3NewsForm, self).__init__(*args, **kwargs)  
                    self.fields['newspart'].choices = [('', line)] + [
                        (part.id, '%s / %s' % (part.part,part.realPart)) ]
                    
            linkForm = this_LinkNewsForm()
            textForm = this_TextNewsForm()
            picForm = this_PicNewsForm()
            mp3Form = this_mp3NewsForm()
            
        return render_to_response('newsSubmit.html',locals(),
            context_instance=RequestContext(request)) 
    if request.method == 'POST':
        this_user = request.user
        type = request.POST.get('type')
        if type == 'link':
            form = LinkNewsForm(request.POST,request.FILES)
            if form.is_valid():
                this_news = News(
                    user = this_user,
                    type = form.cleaned_data['type'],
                    title = form.cleaned_data['title'],
                    agree_man = '%s;' % this_user.id,
                    link = form.cleaned_data['link'],
                    newspart = form.cleaned_data['newspart'],
                    open = form.cleaned_data['newspart'].open,
                    secret=form.cleaned_data['newspart'].secret,
                    ups = 1,
                    downs = 0, 
                    read = 0,
                    gold = 0,
                    score = 1,
                    controversy = controversy(0, 0),
                    hot = 0,
                    comment_num = 0
                )
                this_news.save()
                this_news.hot = hot(1, 0, 0,this_news.time)
                this_news.save()
                add_part = form.cleaned_data['newspart']
                add_part.num += 1
                add_part.save()
                part_All.num += 1
                part_All.save()
                this_user.money += 6
                this_user.save()
            else:
                return render_to_response('newsSubmit.html',locals(),
                    context_instance=RequestContext(request))
        elif type == 'text':
            form = TextNewsForm(request.POST,request.FILES)
            if form.is_valid():
                this_news = News(
                    user = this_user,
                    type = form.cleaned_data['type'],
                    title = form.cleaned_data['title'],
                    agree_man = '%s;' % this_user.id,
                    text = form.cleaned_data['text'],
                    newspart = form.cleaned_data['newspart'],
                    open = form.cleaned_data['newspart'].open,
                    secret=form.cleaned_data['newspart'].secret,
                    ups = 1,
                    downs = 0,              
                    gold = 0,
                    read = 0,
                    score = 1,
                    controversy = controversy(0, 0),
                    hot = 0,
                    comment_num = 0
                )
                this_news.save()
                this_news.hot = hot(1, 0, 0,this_news.time)
                this_news.save()
                add_part = form.cleaned_data['newspart']
                add_part.num += 1
                add_part.save()
                part_All.num += 1
                part_All.save()
                this_user.money += 10
                this_user.save()
            else:
                return render_to_response('newsSubmit.html',locals(),
                    context_instance=RequestContext(request))
        elif type == 'pic':
            form = PicNewsForm(request.POST,request.FILES)
            if form.is_valid():
                this_news = News(
                    user = this_user,
                    type = form.cleaned_data['type'],
                    title = form.cleaned_data['title'],
                    agree_man = '%s;' % this_user.id,
                    #pic = form.cleaned_data['pic'],
                    newspart = form.cleaned_data['newspart'], 
                    open = form.cleaned_data['newspart'].open,
                    secret=form.cleaned_data['newspart'].secret,
                    ups = 1,
                    downs = 0,              
                    gold = 0,
                    score = 1,
                    read = 0,
                    controversy = controversy(0, 0),
                    hot = 0,
                    comment_num = 0
                )
                this_news.save()
                this_news.hot = hot(1, 0, 0,this_news.time)
                this_news.save()
                add_part = form.cleaned_data['newspart']
                add_part.num += 1
                add_part.save()
                part_All.num += 1
                part_All.save()
                this_user.money += 10
                this_user.save()             
            else:
                return render_to_response('newsSubmit.html',locals(),
                    context_instance=RequestContext(request))
        else:
            form = mp3NewsForm(request.POST,request.FILES)        
            if form.is_valid():
                this_news = News(
                    user = this_user,
                    type = form.cleaned_data['type'],
                    title = form.cleaned_data['title'],
                    agree_man = '%s;' % this_user.id,
                    #mp3 = form.cleaned_data['mp3'],
                    newspart = form.cleaned_data['newspart'],
                    open = form.cleaned_data['newspart'].open,
                    secret=form.cleaned_data['newspart'].secret,
                    ups = 1,
                    downs = 0,              
                    gold = 0,
                    score = 1,
                    read = 0,
                    controversy = controversy(0, 0),
                    hot = 0,
                    comment_num = 0
                )
                this_news.save()
                this_news.hot = hot(1, 0, 0,this_news.time)
                this_news.save()
                add_part = form.cleaned_data['newspart']
                add_part.num += 1
                add_part.save()
                part_All.num += 1
                part_All.save()
                this_user.money += 10
                this_user.save()
            else:
                return render_to_response('newsSubmit.html',locals(),
                    context_instance=RequestContext(request))
        
        this_user_info.upVoted_news += '%s;' % this_news.id
        this_user_info.save()
        
        
        this_feeds = Feeds_followNews(
            type = 'followNews',
            owner = this_user,
            showText = True,
            creator = this_user,
            news = this_news
        )
        this_feeds.save()
        #this_feeds.owner.message += 1
        #this_feeds.owner.save()
        if this_user_info.beWatched:
            beWatched_list = this_user_info.beWatched.split(';')[:-1]
            users = MyUser.objects.filter(id__in=beWatched_list)       
            for watching_user in users:
                this_feeds = Feeds_followNews(
                    type = 'followNews',
                    owner = watching_user,
                    showText = True,
                    creator = this_user,
                    news = this_news
                )
                this_feeds.save()
                this_feeds.owner.message += 1
                this_feeds.owner.save()
        
        if type == 'pic' or type == 'mp3':
            url = '/news/uploadFile/%s/%s/' % (type,this_news.id)
            return HttpResponseRedirect(url)
        url = '/news/'+ news_part + '/hot/showNews/%s/' % this_news.id
        return HttpResponseRedirect(url)
       
def show_news(request,news_part,small_part,news_id):             
    user = request.user
    newsHTML = True
    this_small_part = small_part
    allNewsPart = NewsPart.objects.all()
    newsParts = allNewsPart.filter(open=True,secret=False).order_by('-num','-user_num','part')   
    top_newsParts = newsParts[:18]
    more_newsParts = newsParts[18:]
    if user.is_authenticated():
        this_user_info = User_info.objects.get(user=user)
        subscriptions = this_user_info.subscription.split(';')[:-1]
        mySubs = allNewsPart.filter(part__in=subscriptions).order_by('part')
    else:
        defaultList = ['Funny','Life','Music','Home-news','SuggestCY','Gossip']
        mySubs = allNewsPart.filter(part__in=defaultList).order_by('part')
    
    
    this_news = News.objects.get(id=news_id)

    read = this_news.read + 1
    ups = this_news.ups
    downs = this_news.downs
    this_news.read = read
    this_news.hot = hot(ups, downs, read, this_news.time)
    this_news.save()
            
    if this_news.type == 'pic':
        newspics = NewsPic.objects.filter(news=this_news)
        picnum = newspics.count()
        if picnum > 15:
            return render_to_response('404.html',locals(),
                context_instance=RequestContext(request))     
        if picnum >12:
            picnum13_15 = True
            picnum10_12 = True
            picnum7_9 = True
            picnum4_6 = True            
            picgroup1 = newspics[:3]
            picgroup2 = newspics[3:6]
            picgroup3 = newspics[6:9]
            picgroup4 = newspics[9:12]
            picgroup5 = newspics[12:15]
        if picnum >9:
            picnum10_12 = True
            picnum7_9 = True
            picnum4_6 = True            
            picgroup1 = newspics[:3]
            picgroup2 = newspics[3:6]
            picgroup3 = newspics[6:9]
            picgroup4 = newspics[9:12]
        elif picnum > 6:
            picnum7_9 = True
            picnum4_6 = True
            picgroup1 = newspics[:3]
            picgroup2 = newspics[3:6]
            picgroup3 = newspics[6:9]
        elif picnum > 3:
            picnum4_6 = True
            picgroup1 = newspics[:3]
            picgroup2 = newspics[3:6]
        else:
            picgroup1 = newspics[:3]
    if (this_news.ups+this_news.downs) != 0:
        percent = float(this_news.ups) / abs(this_news.ups+this_news.downs)
        ratioLink = '%.0f%%' % (percent*100)
    else:
        ratioLink = 0
    if user.is_authenticated():
        if user == this_news.user:
            need_log = False
            need_vote = False
            need_money = False
        elif user.money < 1:
            need_log = False
            need_vote = False
            need_money = True
        else:
            this_user_info = User_info.objects.get(user=user)
            if news_id in this_user_info.upVoted_news or news_id in this_user_info.downVoted_news:
                need_log = False
                need_vote = False
                need_money = False
            else:
                need_log = False
                need_vote = True
                need_money = False
    else:
        need_log = True
        need_vote = False
        need_money = False
    part = this_news.newspart
    SimilarHtml = 'Similar' + part.part + '.html'
    
    if news_part != 'All':
        newses = News.objects.filter(newspart=part)
    else:
        newses = News.objects.filter(open=True,secret=False)
    
    def cut(arr, indices):  
        return [arr[i:j] for i, j in zip([0]+indices, indices+[None])]  
                
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    day = today.day
    _weekday,_lastday = calendar.monthrange(year,month)  
    _sundays = [x for x in range(6-_weekday+1,_lastday+1,7)]  

    weekList =  cut(range(1,_lastday+1),_sundays)

    for index, item in enumerate(weekList):
        if day in item:
            this_week = item
            break

    start_date = datetime.datetime(year,month,this_week[0],0,0,0,0)
    end_date = datetime.datetime.today()
    weekTopList = newses.filter(time__range=(start_date, end_date)).order_by('-score','-time')[:8]
    
    Comment1 = NewsComment1.objects.all()
    Comment2 = NewsComment2.objects.all()
    comments = sorted(list(Comment1) + list(Comment2), key=lambda x: x.time,reverse = True)
    newComments = comments[:6]
    
    return render_to_response('newsShow.html',locals(),
        context_instance=RequestContext(request))

def getTopPart(request):
    if request.is_ajax() and request.method == 'GET':
        if 'partname' in request.GET:        
            smallPart = 'hot'
            user = request.user
            partname = request.GET.get('partname')
            allNewsPart = NewsPart.objects.all()
            part = allNewsPart.get(part=partname)
            if partname != 'All':
                newses = News.objects.filter(newspart=part)
            else:
                newses = News.objects.filter(open=True,secret=False)
        
            hot_newses = newses.order_by('-hot','-time')[:25]
            controversial_newses = newses.order_by('-controversy','-time')[:25]
            gilded_newses = newses.order_by('-gold','-time')[:30]
            
            top_newses = newses.order_by('-score','-time')[:5]
            
            new_newses = newses.order_by('-time')[:20]
            now = datetime.datetime.now(pytz.utc)
            new_newslist = []

            for news in new_newses: 
                if (now - news.time).total_seconds() < 43200.0:
                    new_newslist.append(news)
            
            return render_to_response('callTopPart.html',locals(),
                context_instance=RequestContext(request))
            
@login_required(login_url='/log/') 
def giveGold(request):
    if request.is_ajax() and request.method == 'GET':
        if 'id' in request.GET:
            if request.user.money > 5:
                this_id = request.GET.get('id')
                this_type = request.GET.get('type')
                if this_type == 'news':
                    this_object = News.objects.get(id=this_id)
                    try:
                        this_feed = Feeds_news.objects.get(
                            type = 'newsGiveGold',
                            owner = this_object.user,
                            creator = request.user,
                            news = this_object                       
                        )
                        this_feed.gold_num += 5
                    except:
                        this_feed = Feeds_news(
                            type = 'newsGiveGold',
                            owner = this_object.user,
                            showText = True,
                            creator = request.user,
                            news = this_object,  
                            gold_num = 5                                    
                        )
                elif this_type == 'newscomment1':
                    this_object = NewsComment1.objects.get(id=this_id)
                    try:
                        this_feed = Feeds_comment.objects.get(
                            type = 'comment1GiveGold',
                            showText = False,
                            owner = this_object.user,
                            creator = request.user,
                            news = this_object.news,
                            newscomment1 = this_object,             
                        )
                        this_feed.gold_num += 5
                    except:
                        this_feed = Feeds_comment(
                            type = 'comment1GiveGold',
                            showText = False,
                            owner = this_object.user,
                            creator = request.user,
                            news = this_object.news,
                            newscomment1 = this_object,
                            gold_num = 5                            
                        )
                elif this_type == 'newscomment2':
                    this_object = NewsComment2.objects.get(id=this_id)
                    try:
                        this_feed = Feeds_comment.objects.get(
                            type = 'comment2GiveGold',
                            showText = False,
                            owner = this_object.user,
                            creator = request.user,
                            news = this_object.newscomment1.news,
                            newscomment2 = this_object,             
                        )
                        this_feed.gold_num += 5
                    except:
                        this_feed = Feeds_comment(
                            type = 'comment2GiveGold',
                            showText = False,
                            owner = this_object.user,
                            creator = request.user,
                            news = this_object.newscomment1.news,
                            newscomment2 = this_object,
                            gold_num = 5                            
                        )
                elif this_type == 'newscomment3':
                    this_object = NewsComment3.objects.get(id=this_id)
                    try:
                        this_feed = Feeds_comment.objects.get(
                            type = 'comment3GiveGold',
                            showText = False,
                            owner = this_object.user,
                            creator = request.user,
                            news = this_object.newscomment2.newscomment1.news,
                            newscomment3 = this_object,             
                        )
                        this_feed.gold_num += 5
                    except:
                        this_feed = Feeds_comment(
                            type = 'comment3GiveGold',
                            showText = False,
                            owner = this_object.user,
                            creator = request.user,
                            news = this_object.newscomment2.newscomment1.news,
                            newscomment3 = this_object,
                            gold_num = 5                            
                        )
                else:
                    this_object = NewsComment4.objects.get(id=this_id)
                    try:
                        this_feed = Feeds_comment.objects.get(
                            type = 'comment4GiveGold',
                            showText = False,
                            owner = this_object.user,
                            creator = request.user,
                            news = this_object.newscomment3.newscomment2.newscomment1.news,
                            newscomment4 = this_object,             
                        )
                        this_feed.gold_num += 5
                    except:
                        this_feed = Feeds_comment(
                            type = 'comment4GiveGold',
                            showText = False,
                            owner = this_object.user,
                            creator = request.user,
                            news = this_object.newscomment3.newscomment2.newscomment1.news,
                            newscomment4 = this_object,
                            gold_num = 5                            
                        )
                if this_object.user == request.user:
                    response = HttpResponse('0')
                    return response
                else:
                    this_feed.save()
                    this_feed.owner.message += 1
                    this_feed.owner.save()
                    this_user_info = User_info.objects.get(user=this_object.user)
                    this_object.user.money += 5
                    this_object.user.save()
                    this_object.gold += 5
                    this_object.save()
                    request.user.money -= 5
                    request.user.save()
                    if this_type == 'news':
                        response = HttpResponse(this_user_info.when_newsbeGold)
                    else:
                        response = HttpResponse(this_user_info.when_commentbeGold)
                    return response 
            else:
                response = HttpResponse('-1')
                return response

@login_required(login_url='/log/')                 
def reply(request):
    if request.is_ajax() and request.method == 'GET':
        if 'id' in request.GET:
            this_id = request.GET.get('id')
            this_type = request.GET.get('type')
            return render_to_response('reply.html',locals(),
                context_instance=RequestContext(request))

@login_required(login_url='/log/')                 
def comment(request):
    if request.is_ajax() and request.method == 'GET':
        user = request.user
        if 'comment' in request.GET:    
            try:
                if 'news_id' in request.GET:
                    this_news_id = request.GET.get('news_id')
                    this_news = News.objects.get(id=this_news_id)
                    this_comment = request.GET.get('comment')
                    type = 'newscomment1'
                    this_newComment = NewsComment1(
                        user = user,
                        ups = 0,
                        downs = 0,
                        score = 0,
                        confidence = confidence(0, 0),
                        news = this_news,
                        gold = 0,
                        words = this_comment
                    )
                    this_newComment.save()
                    this_news.comment_num += 1
                    this_news.save()
                    noSuojin = True
                    if this_news.user != user:
                        this_feed = Feeds_news(
                            type = 'newsComment',
                            owner = this_news.user,
                            creator = user,
                            showText = True,
                            news = this_news,             
                            gold_num = 0,
                            comment = this_newComment
                        )
                        this_feed.save()
                        this_feed.owner.message += 1
                        this_feed.owner.save()
            except:
                f=open("D:\comment.txt",'a')   
                traceback.print_exc(file=f)   
                f.flush()   
                f.close()
        if 'type' in request.GET:
            noSuojin = False
            this_type = request.GET.get('type')
            id = request.GET.get('id')
            this_words = request.GET.get('words')
            if this_type == 'newscomment1':
                this_comments1 = NewsComment1.objects.get(id=id)
                this_news = this_comments1.news
                this_newComment = NewsComment2(
                    user = user,
                    ups = 0,
                    downs = 0,
                    score = 0,
                    confidence = confidence(0, 0),
                    newscomment1 = this_comments1,
                    gold = 0,
                    words = this_words
                )
                this_newComment.save()
                type = 'newscomment2'
                if this_news.user != user:
                    this_news.comment_num += 1
                    this_news.save()
                if this_comments1.user != user:
                    this_feed = Feeds_comment(
                        type = 'FComment1Reply',
                        owner = this_comments1.user,
                        news = this_news,
                        showText = False,
                        creator = user,
                        newscomment1 = this_comments1,                      
                        gold_num = 0,
                        comment2 = this_newComment
                    )
                    this_feed.save()
                    this_feed.owner.message += 1
                    this_feed.owner.save()
            if this_type == 'newscomment2':
                this_comments2 = NewsComment2.objects.get(id=id)
                this_news = this_comments2.newscomment1.news
                this_newComment = NewsComment3(
                    user = user,
                    ups = 0,
                    downs = 0,
                    score = 0,
                    confidence = confidence(0, 0),
                    newscomment2 = this_comments2,
                    gold = 0,
                    words = this_words
                )
                this_newComment.save()
                type = 'newscomment3'
                if this_news.user != user:
                    this_news.comment_num += 1
                    this_news.save()
                if this_comments2.user != user:
                    this_feed = Feeds_comment(
                        type = 'FComment2Reply',
                        owner = this_comments2.user,
                        creator = user,
                        showText = False,
                        news = this_news,
                        newscomment2 = this_comments2,                      
                        gold_num = 0,
                        comment3 = this_newComment
                    )
                    this_feed.save()
                    this_feed.owner.message += 1
                    this_feed.owner.save()
            if this_type == 'newscomment3':
                this_comments3 = NewsComment3.objects.get(id=id)
                this_news = this_comments3.newscomment2.newscomment1.news
                this_newComment = NewsComment4(
                    user = user,
                    ups = 0,
                    downs = 0,
                    score = 0,
                    confidence = confidence(0, 0),
                    newscomment3 = this_comments3,
                    gold = 0,
                    words = this_words
                )
                this_newComment.save()
                type = 'newscomment4'
                if this_news.user != user:
                    this_news.comment_num += 1
                    this_news.save()
                if this_comments3.user != user:
                    this_feed = Feeds_comment(
                        type = 'FComment3Reply',
                        owner = this_comments3.user,
                        creator = user,
                        showText = False,
                        news = this_news,
                        newscomment3 = this_comments3,                      
                        gold_num = 0,
                        comment4 = this_newComment
                    )
                    this_feed.save()
                    this_feed.owner.message += 1
                    this_feed.owner.save()
        return render_to_response('comment.html',locals(),
            context_instance=RequestContext(request))

@login_required(login_url='/log/')                 
def commentVote(request):
    if request.is_ajax() and request.method == 'GET':
        if 'vote' in request.GET:
            user = request.user
            type = request.GET.get('type')
            id = request.GET.get('id')
            vote = request.GET.get('vote')
            this_user_info = User_info.objects.get(user=user)
            s = '%s;' % id
            if  type == 'newscomment1':
                this_object = NewsComment1.objects.get(id=id)
                upVoted = 'upVoted_comment1'
                downVoted = 'downVoted_comment1'
            elif type == 'newscomment2':
                this_object = NewsComment2.objects.get(id=id)
                upVoted = 'upVoted_comment2'
                downVoted = 'downVoted_comment2'
            elif type == 'newscomment3':
                this_object = NewsComment3.objects.get(id=id)
                upVoted = 'upVoted_comment3'
                downVoted = 'downVoted_comment3'
            else:
                this_object = NewsComment4.objects.get(id=id)
                upVoted = 'upVoted_comment4'
                downVoted = 'downVoted_comment4'
                
            if vote == '1':
                if user == this_object.user:
                    response = HttpResponse('wrong')
                    return response
                else:
                    ups = this_object.ups + 1            
                    downs = this_object.downs
                    setattr(this_user_info,upVoted, (getattr(this_user_info,upVoted)+s))
                    if getattr(this_user_info,downVoted):
                        if str(this_object.id) in getattr(this_user_info,downVoted):
                            response = HttpResponse('wrong')
                            return response
                    this_user_info.save()
                
            elif vote == '0':
                if user == this_object.user:
                    response = HttpResponse('wrong')
                    return response
                else:
                    downs = this_object.downs + 1
                    ups = this_object.ups
                    setattr(this_user_info,downVoted, (getattr(this_user_info,downVoted)+s))
                    if getattr(this_user_info,upVoted):
                        if str(this_object.id) in getattr(this_user_info,upVoted):
                            response = HttpResponse('wrong')
                            return response
                    this_user_info.save()
            else:
                response = HttpResponse('wrong')
                return response
                
            score = ups - downs
            this_object.ups = ups
            this_object.downs = downs
            this_object.score = score
            this_object.confidence = confidence(ups, downs)
            this_object.save()
            
            return render_to_response('commentAfterVote.html',locals(),
                context_instance=RequestContext(request))

@login_required(login_url='/log/') 
def watch(request):
    if request.is_ajax() and request.method == 'GET':
        id = request.GET.get('id')
        s = id + ';'
        news_user = MyUser.objects.get(id=id)
        news_user_info = User_info.objects.get(user=news_user)
        action = request.GET.get('action')
        user = request.user
        this_user_info = User_info.objects.get(user=user)
        if action == '1':
            if id in this_user_info.watching or str(user.id) in news_user_info.beWatched:
                response = HttpResponse(u'哦，出现了点小问题，这可能是外星人造成的，请到【易反馈】反馈这一问题')
                return response
            else:
                this_user_info.watching += s
                news_user_info.beWatched += '%s;' % user.id
                this_user_info.save()
                news_user_info.save()
                
                response = HttpResponse(news_user_info.when_beWatched)
                return response
        if action == '-1':
            if id not in this_user_info.watching or str(user.id) not in news_user_info.beWatched:
                response = HttpResponse(u'哦，出现了点小问题，这可能是外星人造成的，请到【易反馈】反馈这一问题')
                return response
            else:
                this_user_info.watching = this_user_info.watching.replace(s,'')
                news_user_info.beWatched = news_user_info.beWatched.replace('%s;' % user.id,'')
                this_user_info.save()
                news_user_info.save()
                response = HttpResponse(u'已取消关注')
                return response

@csrf_exempt
def ke_upload_view(request):
    
    # 2.5MB - 2621440
    # 5MB - 5242880
    # 10MB - 10485760
    # 20MB - 20971520
    # 50MB - 52428800
    # 100MB 104857600
    # 250MB - 214958080
    # 500MB - 429916160

    ext_allowed = ['gif', 'jpg', 'jpeg', 'png','PNG','GIF','JPG','JPEG']
    max_size = 4194304 # 4M
    today = datetime.datetime.today()
    save_dir = '/news_TextPic/%d/%d/%d/' % (today.year, today.month, today.day)
    save_path = settings.MEDIA_ROOT+save_dir
    save_url = settings.MEDIA_URL+save_dir
    #print save_dir, save_path, save_url

    if request.method == 'POST':
        file = request.FILES['imgFile']
        
        if not file.name:
            return HttpResponse(json.dumps(
                { 'error': 1, 'message': u'请选择要上传的文件' }
            ))

        ext = file.name.split('.').pop()
        if ext not in ext_allowed:
            return HttpResponse(json.dumps(
                { 'error': 1, 'message': u'请上传后缀为%s的文件' %  ext_allowed}
            ))

        if file.size > max_size:
            return HttpResponse(json.dumps(
                { 'error': 1, 'message': u'上传的文件大小不能超过4MB'}
            ))

        if not os.path.isdir(save_path):
            os.makedirs(save_path)


        new_file = '%s.%s' % (int(time.time()), ext)

        destination = open(save_path+new_file, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()

        return HttpResponse(json.dumps(
                { 'error': 0, 'url': save_url+new_file}
        ))

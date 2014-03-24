#coding:utf-8

import urllib
import urllib2
from django.shortcuts import render_to_response
from django.template import RequestContext
from account.models import MyUser
from News.views import which_news
from django.http import HttpResponseRedirect, HttpResponse
from Business.views import AuthorLog
from django.contrib.auth import authenticate, login, logout


def _get_referer_url(request):
    referer_url = request.META.get('HTTP_REFERER', '/')
    host = request.META['HTTP_HOST']
    if referer_url.startswith('http') and host not in referer_url:
        referer_url = '/'
    return referer_url

 
def get_access_token(code):
    auth_url = 'https://graph.qq.com/oauth2.0/token'
    body = urllib.urlencode({
                'code': code, # 授权码
                'client_id': '101046076',
                'client_secret': 'de226ed1a4e71c8f773423575bf116eb',
                'redirect_uri': 'funqiu.com',
                'grant_type': 'authorization_code' # 必须是这个值
                })
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    req = urllib2.Request(auth_url, body, headers)
    resp = urllib2.urlopen(req)
     
    data = json.loads(resp.read())
     
    return data['access_token']    

def get_user_openid(access_token):
    if access_token:
        userinfo_url = 'https://graph.qq.com/oauth2.0/me'
        query_string = urllib.urlencode({'access_token': access_token})
         
        resp = urllib2.urlopen("%s?%s" % (userinfo_url, query_string))
        data = json.loads(resp.read())
        print 'hehehehheh'
        return data    
   
def get_user_nicname(access_token,openid):
    if access_token and openid:
        userinfo_url = 'https://graph.qq.com/user/get_user_info'
        query_string = urllib.urlencode({
            'access_token': access_token,
            'oauth_consumer_key':'101046076',
            'openid':openid
            })
         
        resp = urllib2.urlopen("%s?%s" % (userinfo_url, query_string))
        data = json.loads(resp.read())

        return data
   
def QQ_login(request):
    QQ_auth_url = '%s?%s' % ('https://graph.qq.com/oauth2.0/authorize',
         urllib.urlencode({
             'response_type': 'code',
             'client_id': '101046076',
             'redirect_uri': 'funqiu.com',
             'scope': 'get_user_info',
             'state': _get_referer_url(request)
         })
    )
    return HttpResponseRedirect(QQ_auth_url)
    
def fangqiu(request):
    if 'error' in request.GET or 'code' not in request.GET:
        print '2222'
        return which_news(request,'All','hot')
    else:
        print '1111'
        code = request.GET['code']
     
        access_token = get_access_token(code)
        openid = get_user_openid(access_token)['openid']
        nicname = get_user_nicname(access_token,openid)
        
        print 'openid:%s' % openid
        
        try:
            this_AuthorLog = AuthorLog.objects.get(
                openid =  openid,
                type = 'QQ'
            )
            this_user = this_AuthorLog.user
        except:
            this_user = MyUser.objects.create_user(
                stu_pwd = '123',
                email = '%s@qq1.com' % openid,
                nic_name = nicname,
                money = 100,
                avatar = 'img/avatar.png',
                agree_num = 0,
                message = 0
            )
            this_user.save()
            
            this_user_info = User_info(
                user = this_user,
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
                when_beWatched = u'感谢关注：）'
            )
            this_user_info.save()
            this_AuthorLog = AuthorLog(
                openid =  openid,
                type = 'QQ',
                user = this_user
            )
            this_AuthorLog.save()  
        user = authenticate(username=this_user.email, password=this_user.stu_pwd)
        login(request, user)
        next = '/news/All/hot/'
        if 'state' in request.GET:
            next = request.GET['state']
         
        return HttpResponseRedirect(next)

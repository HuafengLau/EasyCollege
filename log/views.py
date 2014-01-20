#coding:utf-8

import urllib
import urllib2
import chardet 
import bs4
import cookielib
from django.conf import settings
from bs4 import BeautifulSoup
from django import forms
from django.contrib.auth import authenticate, login, logout
from account.models import MyUser
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from University.models import University_info
from DjangoCaptcha import Captcha
from Affair.views import send_mail
import PIL 

from_email = settings.EMAIL_HOST_USER

def deal_register(request):
    _code = request.POST.get('verify') or ''
    if not _code:
        register_message = u'你没有填写验证码！'
        return render_to_response('register.html',locals(),context_instance=RequestContext(request))

    ca = Captcha(request)
    if ca.check(_code):
        pass
    else:
        register_message = u'验证码错误！'
        return render_to_response('register.html',locals(),context_instance=RequestContext(request))
        
    if request.POST['major'].endswith(u'专业'):
        real_major = request.POST['major'][:-2]
    else:
        real_major = request.POST['major']
    try:
        new_university_info = University_info.objects.get(
            school = request.POST['school'],
            college = request.POST['college'],
            major = real_major
        )
    except University_info.DoesNotExist:               
        new_university_info = University_info(
            school = request.POST['school'],
            college = request.POST['college'],
            major = real_major
        )
        new_university_info.save()
        
    finally:
        new_university_info_id = new_university_info.id
    
    try:
        exist_user = MyUser.objects.get(email=request.POST['email'])
        register_message = u'该邮箱已存在，直接登录或者换一个邮箱注册！'
        return render_to_response('register.html',locals(),context_instance=RequestContext(request))
    except:
        pass
    
    try:
        new_user = MyUser.objects.create_user(
            university_info_id = new_university_info_id,
            stu_ID = request.POST['stu_ID'],
            stu_pwd = request.POST['stu_pwd'],
            email = request.POST['email'],
            name = '',
            nic_name = u'某某同学',
            money = '0',
            first_value = '0',
            avatar = 'img/avatar.png'           
            
        )
        new_user.save()
        print 'new user saved'
        #username = new_user.email
        #password = new_user.stu_pwd
        #user = authenticate(username=username, password=password)
        #login(request, user)               
        
        #next = '/index/'
        #refreshTime = '1'
        #refreshMessage = u'Loading……您为首次登陆，大学易可能需要一些时间来初始化数据，请稍候……'
    
        email = new_user.email 
        id = new_user.id
        subject = u'账户激活确认'
        text_content = u'请激活您的账户'
        recipient_list = [email,]        
        this_html = loader.render_to_string('remindActivate.html', {
            'id':id,
            }
        )
        send_mail(subject, text_content, from_email, recipient_list, html_content=this_html)
        
        print 'send activateUser.html successfully'
        
        if '@sina.com' in email:
            email_add = 'http://mail.sina.com.cn/'
        elif '@163.com' in email:
            email_add = 'http://mail.163.com/'
        elif '@139.com' in email:
            email_add = 'http://mail.10086.cn/'
        elif '@sohu.com' in email:
            email_add = 'http://mail.sohu.com/'
        elif '@qq.com' in email:
            email_add = 'https://mail.qq.com/cgi-bin/loginpage'
        elif '@126.com' in email:
            email_add = 'http://www.126.com/'
        elif '@sogou.com' in email:
            email_add = 'http://mail.sogou.com/'
        else:
            email_add = None
            
        return render_to_response('activateUser.html',locals(),
            context_instance=RequestContext(request))
    except Exception, e:
        print e
        return render_to_response('404.html',locals(),
            context_instance=RequestContext(request))
    
        
    
def register(request):
    if request.method == 'POST': 
        if 'stu_ID' in request.POST:
            if request.POST['school'] == u'四川大学':
                try:
                    test_answer = judge(request.POST['stu_ID'],request.POST['stu_pwd'])
                    if not test_answer:
                        register_message = u'学生系统账号或密码错误！抱歉，您可能需要重新填写注册表单'
                        return render_to_response('register.html',locals(),context_instance=RequestContext(request))
                    else:
                        return deal_register(request)
                except:
                    register_message = u'运气太差！访问川大教务系统被拒绝，建议使用校园网或者攒人品稍候再试。'
                    return render_to_response('register.html',locals(),context_instance=RequestContext(request))               
            else:
                return deal_register(request)
    
def judge(zh,mm):
    login_page = 'http://202.115.47.141/loginAction.do'
    url_ttable = 'http://202.115.47.141/xkAction.do?actionType=6'

    cj = cookielib.CookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        
    data = urllib.urlencode({"zjh":zh,"mm":mm})
        
    request = urllib2.Request(login_page, data)
    request.add_header('User=Agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0')
    response = opener.open(request)
    next = opener.open(url_ttable)
    doc=next.read()
    doc_encoding = chardet.detect(doc)['encoding']
    soup = BeautifulSoup(''.join(doc), from_encoding=doc_encoding)
    if soup.find('font', {'color':'#990000'}) == None:
        return True
    else:
        return False
    
def log(request):     
    if request.method == 'POST':    
        username = request.POST['email']
        password = request.POST['stu_pwd']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if 'next' in request.POST:               
                    next = request.POST['next']
                    refreshTime = '3'
                    refreshMessage = u'Loading……3秒后返回登录前页面'
                    return render_to_response('nextPage.html',locals(),
                        context_instance=RequestContext(request))
                    #return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect('/index/')
            else:
                wrong_not_active = u'该账号未被激活或者已被禁用'
                return render_to_response('log.html',locals(),
                    context_instance=RequestContext(request))
        else:
            wrong_not_exist = u'账号或密码错误!'
            return render_to_response('log.html',locals(),
                context_instance=RequestContext(request))
    else:
        next = request.GET.get('next')
        return render_to_response('log.html',locals(),
            context_instance=RequestContext(request))

def page_register(request):
    return render_to_response('register.html',locals(),
        context_instance=RequestContext(request))
       
def quit(request):
    logout(request)   
    return HttpResponseRedirect('/log/')
    
def verify(request):
    ca =  Captcha(request)
    ca.words = ['collegeyi','college','daxueyi','xuanke']
    ca.type = 'word'
    return ca.display()
    
def activateUser(request, id):
    try:
        this_user = MyUser.objects.get(id=id)
        this_user.is_active = True
        this_user.save()
        
        username = this_user.email
        password = this_user.stu_pwd
        user = authenticate(username=username, password=password)
        login(request, user)               
        
        university_info = University_info.objects.get(id=this_user.university_info_id)
        if university_info.school == u'四川大学':         
            next = '/index/'
            refreshTime = '1'
            moreMessage = u'恭喜您成功激活账户！'
            refreshMessage = u'Loading……对于首次登陆的川大用户，大学易可能需要一些时间来初始化数据，请稍候……'
            
            return render_to_response('nextPage.html',locals(),
                context_instance=RequestContext(request))
        else:
            next = '/index/'
            refreshTime = '3'
            moreMessage = u'恭喜您成功激活账户！'
            refreshMessage = u'Loading……3s后跳转到主页，请稍候……'
            
            return render_to_response('nextPage.html',locals(),
                context_instance=RequestContext(request))
    except:
        return render_to_response('404.html',locals(),
            context_instance=RequestContext(request))
    



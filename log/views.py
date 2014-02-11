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
from Center.models import User_info
from django.contrib.auth.decorators import login_required

school_code = {u'华东师范大学':'ecnu',u'赣南师范学院':'gnnu',u'内蒙古师范大学':'imnu',
    u'西北农林科技大学':'nwsuaf',u'北京信息科技大学':'bistu',u'江西财经大学':'jxufe',u'西昌学院':'xcc',
    u'西华大学':'xhu'}

URP_school = [u'四川大学', u'安徽财经大学']

wise_school = [u'华东师范大学',u'赣南师范学院',u'内蒙古师范大学',u'西北农林科技大学',
    u'北京信息科技大学',u'江西财经大学',u'西昌学院',u'西华大学']   

from_email = settings.EMAIL_HOST_USER
    
def deal_register(request):
    _code = request.POST.get('verify') or ''
    if not _code:
        register_message = u'你没有填写验证码！'
        return render_to_response('register_step1.html',locals(),context_instance=RequestContext(request))

    ca = Captcha(request)
    if ca.check(_code):
        pass
    else:
        register_message = u'验证码错误！'
        return render_to_response('register_step1.html',locals(),context_instance=RequestContext(request))
        
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
        return render_to_response('register_step1.html',locals(),context_instance=RequestContext(request))
    except:
        pass
    
    try:
        new_user = MyUser.objects.create_user(
            university_info_id = new_university_info_id,
            stu_ID = '000000',
            stu_pwd = request.POST['stu_pwd'],
            email = request.POST['email'],
            name = '',
            nic_name = u'某某同学',
            money = '0',
            first_value = '0',
            avatar = 'img/avatar.png'           
            
        )
        new_user.save()
        
        this_user_info = User_info(
            store_eot = '',
            user = new_user,
            download_Eotdata = '',
            nocomment_Eotdata = '',
            grade = u'公民'
        )
        this_user_info.save()
    
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
            
        return render_to_response('register_step2.html',locals(),
            context_instance=RequestContext(request))
    except Exception, e:
        print e
        return render_to_response('404.html',locals(),
            context_instance=RequestContext(request))
       
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
    return render_to_response('register_step1.html',locals(),
        context_instance=RequestContext(request))
        
def verify_email(request):
    if request.is_ajax() and request.method == 'GET':
        if 'email' in request.GET:
            this_email = request.GET.get('email')
            try:
                yes_email = MyUser.objects.get(email=this_email)
                response = HttpResponse("<span class='glyphicon glyphicon-remove font-red'> 邮箱已被注册，换一个吧</span>")
                return response
            except:
                response = HttpResponse("<span class='glyphicon glyphicon-ok font-green'> 邮箱可用，注册后我们将向其发送激活邮件</span>")
                return response
        else:
            print e
            return render_to_response('500.html',locals(),
                context_instance=RequestContext(request))
    else:
        print e
        return render_to_response('500.html',locals(),
            context_instance=RequestContext(request))

@login_required(login_url='/log/')            
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
  
        return HttpResponseRedirect('/log/register/step3/')
    except:
        return render_to_response('404.html',locals(),
            context_instance=RequestContext(request))

def register_step3(request):
    this_user = request.user
    university_info = University_info.objects.get(id=this_user.university_info_id)
    
    school = university_info.school
    
    if school in URP_school:
        school_type = 'URP'
    elif school in wise_school:
        school_type = 'wise'
        this_school_code = school_code[school]
    else:
        school_type = 'others'
    
    

    return render_to_response('register_step3.html',locals(),
        context_instance=RequestContext(request))
    
    '''if university_info.school == u'四川大学':         
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
            context_instance=RequestContext(request))'''

    



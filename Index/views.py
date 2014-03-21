#coding:utf-8

from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
#from Business.models import Credit, Major_course
#from Business.views import GPA, wise_analyzeCreditFile
#from University.models import University_info
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from Index.form import AvatarForm
from Index.models import Feeds_news,Feeds_comment,Feeds_followNews
from django.conf import settings
from account.models import MyUser
from bs4 import BeautifulSoup
#from log.views import URP_school,wise_school,school_code
from Center.models import Honour
from Center.models import User_info
#from EOT.models import Eot_data
import os
import random
import time
import urllib2
import urllib
import chardet 
import cookielib
import bs4

@login_required(login_url='/log/') 
def index(request):
    user = request.user
    user.message = 0
    user.save()
    Feeds1 = Feeds_followNews.objects.filter(owner=user)
    Feeds2 = Feeds_news.objects.filter(owner=user)
    Feeds3 = Feeds_comment.objects.filter(owner=user)
    Feeds = sorted(list(Feeds1) + list(Feeds2) + list(Feeds3), key=lambda x: x.time,reverse = True)
    
    my_user_info = User_info.objects.get(user=user)
    if my_user_info.watching:
        list1 = my_user_info.watching.split(';')[:-1]
        my_watching = MyUser.objects.filter(id__in=list1)
    if my_user_info.beWatched:
        list2 = my_user_info.beWatched.split(';')[:-1]
        my_beWatched = MyUser.objects.filter(id__in=list2) 
        
    indexHTML = True
    
    return render_to_response('index.html',locals(),
        context_instance=RequestContext(request))
    
def loading_gif(request):
    if request.is_ajax() and request.method == 'GET':
        if 'loading' in request.GET:
            print settings.STATIC_URL
            temp = "<img src='%simg/loading.gif' alt='URP检测'/>" % settings.STATIC_URL
            response = HttpResponse(temp)
            return response

def get_idCard(request):
    if request.is_ajax() and request.method == 'GET':
        if 'id' in request.GET:    
            this_id = request.GET.get('id')
            this_user = MyUser.objects.get(id=this_id)
            this_user_info = User_info.objects.get(user=this_user)
            return render_to_response('idCard.html',locals(),
                context_instance=RequestContext(request))            
        
'''        
def display(request,user,message,HTML):                  
    credits = Credit.objects.filter(user=user)
    if not credits:
        credits = None
    else:
        credits_after_range_num = 5        
        credits_befor_range_num = 4       
        try:                     
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(credits,20)   
        try:                     
            credits_list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            credits_list = paginator.page(paginator.num_pages)
        if page >= credits_after_range_num:
            credits_page_range = paginator.page_range[page-credits_after_range_num:page+credits_befor_range_num]
        else:
            credits_page_range = paginator.page_range[0:int(page)+credits_befor_range_num]
        credits = credits_list
    
    message = message
    
    try:
        if u'源代码' in message or u'数据库' in message:
            no_refresh = True
        else:
            no_refresh = False       
    except:
        no_refresh = False
        
    if message == 'URP':
            school_type = 'URP'
            message = None
    elif message == 'wise':
        school_type = 'wise'
        university_info_id = user.university_info_id
        school = University_info.objects.get(id=university_info_id).school
        attr_need_list = ['nenu','jxufe','sysu']
        this_school_code = school_code[school]
        if this_school_code in attr_need_list:
            attr_need = True
        message = None
    else:
        pass
        
    
    form = AvatarForm()
    indexHTML = True
    rich_users = MyUser.objects.order_by('-money')[:3]
    
    Feeds1 = Feeds_followNews.objects.filter(owner=user)
    Feeds2 = Feeds_news.objects.filter(owner=user)
    Feeds3 = Feeds_comment.objects.filter(owner=user)
    Feeds = sorted(list(Feeds1) + list(Feeds2) + list(Feeds3), key=lambda x: x.time,reverse = True)
    
    my_user_info = User_info.objects.get(user=user)
    if my_user_info.watching:
        list1 = my_user_info.watching.split(';')[:-1]
        my_watching = MyUser.objects.filter(id__in=list1)
    if my_user_info.beWatched:
        list2 = my_user_info.beWatched.split(';')[:-1]
        my_beWatched = MyUser.objects.filter(id__in=list2) 
    
    indexChoice = HTML
    
    return render_to_response('index.html',locals(),
        context_instance=RequestContext(request))

@csrf_exempt
@login_required(login_url='/log/') 
def index(request):
    if request.is_ajax() and request.method == 'POST':
        if 'teacher_name' in request.POST:
           teacher = request.POST.get('teacher_name')
           id = request.POST.get('course_id')
           edit_credit = Credit.objects.get(id=id)
           edit_credit.course_teacher = teacher
           edit_credit.save()
           
           response = HttpResponse()
           return response
         
        if 'teacher_attr' in request.POST:
           attr = request.POST.get('teacher_attr')
           id = request.POST.get('course_id')[:-1]
           edit_credit = Credit.objects.get(id=id)
           edit_credit.course_attr = attr
           edit_credit.save()
           
           response = HttpResponse()
           return response
           
        if 'grade' in request.POST:
            user = request.user
            grade = request.POST.get('grade')
            name = request.POST.get('name')
            teacher = request.POST.get('teacher')
            attr = request.POST.get('attr')
            try:
                credit = float(request.POST.get('credit'))
                score = float(request.POST.get('score'))
            except:
                response = HttpResponse()
                return response
           
            try:
                Credit.objects.get(
                    course_name = name,
                    grade = grade,
                    user = user
                )
                response = HttpResponse()
                return response
            except:
                credit = Credit(
                    course_name = name,
                    course_teacher = teacher,
                    course_credit = credit,
                    course_attr = attr,
                    course_score = score,                
                    add_money = 0,    
                    grade = grade,  
                    user = user
                )
                credit.save()
                if attr == u'必修':
                    try:
                        new_major_course = Major_course.objects.get(
                            course_name = credit.course_name,
                            course_teacher = credit.course_teacher,
                            major_id = user.university_info_id
                        )
                    except:
                        new_major_course = Major_course(
                            course_name = credit.course_name,
                            course_teacher = credit.course_teacher,
                            major_id = user.university_info_id,
                            course = credit
                        )
                        new_major_course.save()
      
                response = HttpResponse()
                return response
            
        if 'string' in request.POST:
            user = request.user
            string = request.POST.get('string')
            arr = string.split(';')
            grade = arr[0].strip()
            name = arr[1].strip()
            teacher = arr[2].strip()
            attr = arr[3].strip()
            try:
                credit = float(arr[4].strip())
                score = float(arr[5].strip())
            except:
                response = HttpResponse()
                return response
           
            try:
                Credit.objects.get(
                    grade = grade,
                    course_name = name,
                    user = user
                )
                response = HttpResponse()
                return response
            except:
                credit = Credit(
                    course_name = name,
                    course_teacher = teacher,
                    course_credit = credit,
                    course_attr = attr,
                    course_score = score,                
                    add_money = 0,    
                    grade = grade,  
                    user = user
                )
                credit.save()                
                if attr == u'必修':
                    try:
                        new_major_course = Major_course.objects.get(
                            course_name = credit.course_name,
                            course_teacher = credit.course_teacher,
                            major_id = user.university_info_id
                        )
                    except:
                        new_major_course = Major_course(
                            course_name = credit.course_name,
                            course_teacher = credit.course_teacher,
                            major_id = user.university_info_id,
                            course = credit
                        )
                        new_major_course.save()
            money = random.randrange(5,10,1)
            user.money += money
            user.save()
            response = HttpResponse()
            return response
                                
    elif request.is_ajax() and request.method == 'GET':
        if 'wise_add' in request.GET:
            user = request.user
            major_courses = Major_course.objects.filter(major_id=user.university_info_id)
            if major_courses:
                credits = Credit.objects.filter(user=user)
                if credits:
                    for credit in credits:
                        major_courses = major_courses.exclude(
                            course_name = credit.course_name
                            #course_teacher = credit.course_teacher
                        )
                if major_courses:                    
                    message = None
                    select_credit = []
                    major_courses = major_courses.order_by('course_name')
                    for i in xrange(11):
                        select_credit.append(float(i))
                    return render_to_response('wise_course.html',locals(),
                        context_instance=RequestContext(request))
                else:
                    message = u'抱歉，当前没有可以添加的课程'
                    return render_to_response('wise_course.html',locals(),
                        context_instance=RequestContext(request)) 
            else:
                message = u'抱歉，当前没有可以添加的课程'
                return render_to_response('wise_course.html',locals(),
                    context_instance=RequestContext(request)) 


    else:
        #global user
        user = request.user
        university_info_id = user.university_info_id
        school = University_info.objects.get(id=university_info_id).school
        
        if school in URP_school or school in wise_school:
            if school in URP_school:
                message = 'URP'
            else:
                message = 'wise'
            HTML = 'index'
            return display(request,user,message,HTML)   
        else:           
            #credits = Credit.objects.filter(user=user).order_by('grade','add_money')
            message = None
            HTML = 'index2'
            return display(request,user,message,HTML)
         
@login_required(login_url='/log/')
def wise_teacher(request):
    user = request.user
    university_info_id = user.university_info_id
    credits = Credit.objects.filter(user=user,course_teacher='')
    if not credits:
        message = u'所有课程已添加任课老师！'
        HTML = 'index'
        return display(request,user,message,HTML)
        
    else:
        add_num = 0
        for credit in credits:
            yes_credits = Credit.objects.filter(university_info_id=university_info_id, 
                course_name=credit.course_name).exclude(course_teacher='').order_by('-add_date')
            if yes_credits:
                teacher = yes_credits[0].course_teacher
                credit.course_teacher = teacher
                credit.save()
                add_num += 1
        if add_num == 0:
            message = u'暂时没有发现新的可以添加的任课老师。试试手工添加吧！'
            HTML = 'index'
            return display(request,user,message,HTML)
            
        else:
            message = u'学长学姐为您添加了%s位任课老师！' % add_num
            HTML = 'index'
            return display(request,user,message,HTML)
            
@login_required(login_url='/log/')
def del_credit(request, credit_id):
    try:
        this_credit = Credit.objects.get(id=credit_id)
        this_credit.delete()
    except:
        pass
    return HttpResponseRedirect('/index/')

@login_required(login_url='/log/') 
def verify_URP(request):
    if request.is_ajax() and request.method == 'GET':
        if 'zh' in request.GET:
            zh = request.GET.get('zh')
            mm = request.GET.get('mm')
            
            this_user = request.user
            university_info = University_info.objects.get(id=this_user.university_info_id)
            school = university_info.school
            
            if school == u'四川大学':        
                login_page = 'http://202.115.47.141/loginAction.do'
            elif school == u'安徽财经大学':
                login_page = 'http://jwcxk.aufe.edu.cn/loginAction.do'
            else:
                response = HttpResponse(u'警告，未知错误，请联系管理员collegeyi@sina.com')
                return response
            
            cj = cookielib.CookieJar();
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))               
            data = urllib.urlencode({"zjh":zh,"mm":mm})             
            request = urllib2.Request(login_page, data)
            request.add_header('User=Agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0')
            response = opener.open(request)
            doc=response.read()
            doc_encoding = chardet.detect(doc)['encoding']
            soup = BeautifulSoup(''.join(doc), from_encoding=doc_encoding)
            if soup.find('frameset',{'border':"0"}) == None:
                temp = "<p class='text-danger'>该账号和密码无法登陆系统，出现此错误的原因有<ul><li>账号和密码错误，\
                    请重新输入（常见）</li><li>网络问题，请重新输入（偶尔）</li><li>由于教师需录入成绩、系统升级等原因，\
                    当前无法访问学生系统，您可以打开学生教务系统验证一下</li></ul></p>"
                response = HttpResponse("<span class='glyphicon glyphicon-remove font-red'></span>%s" % temp)
                return response
            else:
                response = HttpResponse("<span class='glyphicon glyphicon-ok font-green'> 账号和密码正确</span>")
                return response

            
def add_points(university_info_id,user,points):
    add_num = 0
    for index, item in enumerate(points):
        try:
            score = float(item[3])
            try:
                has_credit = Credit.objects.get(user=user,course_name = item[0])
                continue
            except:
                if item[2] == '':
                    attr = u''
                else:
                    attr = item[2]
                try:
                    teacher = item[4]
                except:
                    teacher = ''
                credit = Credit(
                    course_name = item[0],
                    course_teacher = teacher,
                    course_credit = item[1],
                    course_attr = attr,
                    course_score = score,                
                    add_money = '0',    
                    grade = 'NoIdeal',  
                    user = user,
                    university_info_id = university_info_id
                    
                )
                credit.save()
                add_num += 1
                
                if u'必修' in item[2] or u'专业' in item[2]:
                    try:
                        new_major_course = Major_course.objects.get(
                            course_name = credit.course_name,
                            course_teacher = credit.course_teacher,
                            major_id = user.university_info_id
                        )
                    except:
                        new_major_course = Major_course(
                            course_name = credit.course_name,
                            course_teacher = credit.course_teacher,
                            major_id = user.university_info_id,
                            course = credit
                        )
                        new_major_course.save()
        except:
            continue
    return add_num
        
@login_required(login_url='/log/')             
def URP_getCredit(request):
    user = request.user
    
    zh = request.POST['zh']
    mm = request.POST['mm']
        
    try:
        points = GPA(user,zh,mm)
        add_num = add_points(user.university_info_id,user,points)
        if add_num == 0:
            message = u'本次访问数据库没有发现新的课程数据！'
        else:
            message = u'本次访问数据库为您添加了%s门课程的数据！' % add_num
        HTML = 'index'
        return display(request,user,message,HTML)
    except urllib2.URLError:
        time.sleep(1)
        try:
            points = GPA(user,zh,mm)
            add_num = add_points(user.university_info_id,user,points)
            if add_num == 0:
                message = u'本次访问数据库没有发现新的课程数据！'
            else:
                message = u'本次访问数据库为您添加了%s门课程的数据！' % add_num
            HTML = 'index'
            return display(request,user,message,HTML)
        except urllib2.URLError:
            time.sleep(1)
            try:
                points = GPA(user,zh,mm)
                add_num = add_points(user.university_info_id,user,points)
                if add_num == 0:
                    message = u'本次访问数据库没有发现新的课程数据！'
                else:
                    message = u'本次访问数据库为您添加了%s项新的数据！' % add_num
                HTML = 'index'
                return display(request,user,message,HTML)
            except urllib2.URLError:
                message = u'当前无法访问教务系统，请稍候再试'
                HTML = 'index'
                return display(request,user,message,HTML)

@login_required(login_url='/log/')                
def wise_getCredit(request,school_code):
    user = request.user
    f = request.FILES['credit_file']
    doc = f.read()
    if doc:
        points = wise_analyzeCreditFile(doc,school_code)
        if points:
            add_num = add_points(user.university_info_id,user,points)
            if add_num == 0:
                message = u'未在您本次提交的源代码页面中发现新的数据！'
            else:
                message = u'在您本次提交的源代码页面中，大学易发现了%s项新的数据！' % add_num
            HTML = 'index'
            return display(request,user,message,HTML)
        else:
            message = u'上传的源代码文件有误！如果您确定上传了正确的文件，请联系管理员collegeyi@sina.com'
            HTML = 'index'
            return display(request,user,message,HTML)
    else:
        message = u'上传的源代码文件有误！如果您确定上传了正确的文件，请联系管理员'
        HTML = 'index'
        return display(request,user,message,HTML)
'''
        

        
            
                 
    


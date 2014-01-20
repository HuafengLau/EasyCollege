#coding:utf-8

from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from Business.models import Credit, Major_course
from Business.views import GPA
from University.models import University_info
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from Index.form import AvatarForm
from django.conf import settings
from Index.models import Avatar
import os
import random
from datetime import datetime
from EOT.models import Eot_data
import time
import urllib2


def display(request,user,message,HTML):                  
    credits = Credit.objects.filter(user=user).order_by('grade','-course_teacher','-course_score')
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
        paginator = Paginator(credits,13)   
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
  
    form = AvatarForm()
    indexHTML = True
    return render_to_response(HTML,locals(),
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
            
        if 'nic_name' in request.POST:
            user = request.user
            user.nic_name = request.POST.get('nic_name')
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
        if school == u'四川大学':           
            if not Credit.objects.filter(user=user):     
                year = time.strftime('%Y',time.localtime(time.time()))
                if year != user.stu_ID[:4]:
                    try:
                        points = GPA(user.stu_ID,user.stu_pwd)
                    except urllib2.URLError:
                        time.sleep(1)
                        try:
                            points = GPA(user.stu_ID,user.stu_pwd)
                        except urllib2.URLError:
                            time.sleep(1)
                            points = GPA(user.stu_ID,user.stu_pwd)
                        
                    for index, item in enumerate(points):
                        credit = Credit(
                            course_name = item[0],
                            course_teacher = '',
                            course_credit = item[1],
                            course_attr = item[2],
                            course_score = item[3],                
                            add_money = '0',    
                            grade = 'NoIdeal',  
                            user = user,
                            university_info_id = university_info_id
                            
                        )
                        credit.save()
                        if item[2] == u'必修':
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
                   
                message = None
                HTML= 'index.html'
                return display(request,user,message,HTML)
                     
            else:
                message = None
                HTML = 'index.html'
                return display(request,user,message,HTML)
                
        else:           
            credits = Credit.objects.filter(user=user).order_by('grade','add_money')
            message = None
            HTML = 'index2.html'
            return display(request,user,message,HTML)

            
@login_required(login_url='/log/')
def wise_teacher(request):
    user = request.user
    university_info_id = user.university_info_id
    credits = Credit.objects.filter(user=user,course_teacher='')
    if not credits:
        message = u'所有课程已添加任课老师！'
        HTML = 'index.html'
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
            message = u'暂时没有发现新的可以添加的任课老师！'
            return display(request,user,message)
            
        else:
            message = u'学长学姐为您添加了%s位任课老师！' % add_num
            HTML = 'index.html'
            return display(request,user,message,HTML)
            
@login_required(login_url='/log/')
def del_credit(request, credit_id):
    try:
        this_credit = Credit.objects.get(id=credit_id)
        this_credit.delete()
    except:
        pass
    return HttpResponseRedirect('/index/')

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
        return HttpResponseRedirect('/index/')
            
        

        
          
    
        
        
            
                 
    


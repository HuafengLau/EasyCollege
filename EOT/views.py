#coding:utf-8

from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from Business.models import Credit,Major_course
from EOT.models import *
from Center.models import User_info
from University.models import University_info
from Index.models import Avatar
from Affair.models import Report_eotData
import random
from django.core.urlresolvers import reverse 
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from EOT.form import Eot_dataForm, Eot_imgForm
from django.conf import settings
from django.core.servers.basehttp import FileWrapper  
import mimetypes  
import os
import tempfile, zipfile
import time
import datetime 


def compare_2(a,b):
    if a>= b:
        return a
    else:
        return b
        
def compare_3(a,b,c):
    temp = compare_2(a,b)
    return compare_2(temp, c)

def compare_4(a,b,c,d):
    temp = compare_3(a,b,c)
    return compare_2(temp, d)

def judge_score(score):
    if score < 55.0:
        return 0
    elif score < 60.0:
        return 1
    elif score < 65.0:
        return 2
    elif score < 70.0:
        return 3
    elif score < 75.0:
        return 4
    elif score < 80.0:
        return 5
    elif score < 85.0:
        return 6
    elif score < 90.0:
        return 7
    elif score < 95.0:
        return 8
    else:
        return 9
    
    
def show(request,this_eot,no_eot, credit_id, **kwargs):
    user = request.user
    if not no_eot:
        naming_num = compare_3(this_eot.naming.never_num,
            this_eot.naming.sometimes_num, this_eot.naming.often_num)
        num_all = this_eot.naming.never_num+this_eot.naming.sometimes_num+this_eot.naming.often_num
        if naming_num == this_eot.naming.never_num:
            percent = float(this_eot.naming.never_num) / num_all
            naming_message = u'很少或几乎不点名（%.0f%%）'% (percent*100)
     
        elif naming_num == this_eot.naming.sometimes_num:
            percent = float(this_eot.naming.sometimes_num) / num_all
            naming_message = u'有时点名（%.0f%%）'% (percent*100)
       
        else:
            percent = float(this_eot.naming.often_num) / num_all
            naming_message = u'较多或经常点名（%.0f%%）'% (percent*100)
                      
        if naming_num == this_eot.naming.never_num:
            naming_way_message = False
        else:
            naming_way_num = compare_3(this_eot.naming_way.sign_num,
                this_eot.naming_way.answer_num, this_eot.naming_way.hybrid_num)
            if naming_way_num == this_eot.naming_way.sign_num:
                naming_way_message = u'主要通过签到或念名单'
            elif naming_way_num == this_eot.naming_way.answer_num:
                naming_way_message = u'主要通过点名回答问题'
            else:
                naming_way_message = u'多种方式混合点名'
                
        atmosphere_num = compare_3(this_eot.atmosphere.dead_num,
            this_eot.atmosphere.normal_num, this_eot.atmosphere.active_num)
        num_all = this_eot.atmosphere.dead_num+this_eot.atmosphere.normal_num+this_eot.atmosphere.active_num
        if atmosphere_num == this_eot.atmosphere.dead_num:
            percent = float(this_eot.atmosphere.dead_num) / num_all
            atmosphere_message = u'死气沉沉（%.0f%%）'% (percent*100)
        elif atmosphere_num == this_eot.atmosphere.normal_num:
            percent = float(this_eot.atmosphere.normal_num) / num_all
            atmosphere_message = u'有时活跃，有时沉闷（%.0f%%）'% (percent*100)
        else:
            percent = float(this_eot.atmosphere.active_num) / num_all
            atmosphere_message = u'较活跃或很活跃（%.0f%%）'% (percent*100)
                  
        percent = this_eot.dead_num / float(this_eot.value_num)
        dead_message = u'%.0f%%'% (percent*100)
        
        teach_way_num = compare_4(this_eot.teach_way.PPT_num,this_eot.teach_way.book_num,
            this_eot.teach_way.teacher_num, this_eot.teach_way.hybrid_num)
        if teach_way_num == this_eot.teach_way.PPT_num:
            teach_way_message = u'主要讲PPT'
        elif teach_way_num == this_eot.teach_way.book_num:
            teach_way_message = u'主要讲教材'
        elif teach_way_num == this_eot.teach_way.teacher_num:
            teach_way_message = u'通过讲义或者老师自己发挥'
        else:
            teach_way_message = u'采用多种方式教学'
        
        popularity_num = compare_4(this_eot.popularity.most_num,this_eot.popularity.more_num,
            this_eot.popularity.less_num, this_eot.popularity.nobody_num)
        if popularity_num == this_eot.popularity.most_num:
            popularity_message = u'学生基本上都去上课'
        elif popularity_num == this_eot.popularity.more_num:
            popularity_message = u'大部分学生去上课'
        elif popularity_num == this_eot.popularity.less_num:
            popularity_message = u'很少学生去上课'
        else:
            popularity_message = u'基本没人去上课'
        
        if this_eot.mid_test.yes_num >= this_eot.mid_test.no_num:
            mid_test_message = u'有期中考试'
            
            mid_test_way_num = compare_4(this_eot.mid_test_way.paper_num, this_eot.mid_test_way.open_num,
                this_eot.mid_test_way.pravite_num, this_eot.mid_test_way.inspect_num)
            if mid_test_way_num == this_eot.mid_test_way.paper_num:
                mid_test_way_message = u'闭卷考试'
            elif mid_test_way_num == this_eot.mid_test_way.open_num:
                mid_test_way_message = u'开卷考试'
            elif mid_test_way_num == this_eot.mid_test_way.pravite_num:
                mid_test_way_message = u'布置任务，私下完成后提交'
            else:
                mid_test_way_message = u'堂上作业等其他考察方式'
        else:
            mid_test_message = u'没有期中考试'
            mid_test_way_message = False
        
        final_test_way_num = compare_4(this_eot.final_test_way.paper_num, this_eot.final_test_way.open_num,
            this_eot.final_test_way.pravite_num, this_eot.final_test_way.inspect_num)
        if final_test_way_num == this_eot.final_test_way.paper_num:
            final_test_way_message = u'闭卷考试'
        elif final_test_way_num == this_eot.final_test_way.open_num:
            final_test_way_message = u'开卷考试'
        elif final_test_way_num == this_eot.final_test_way.pravite_num:
            final_test_way_message = u'布置任务，私下完成后提交'
        else:
            final_test_way_message = u'其他考察方式' 

        final_test_degree_percent = this_eot.final_test_degree / float(this_eot.value_num)

            
        reveal_num = compare_4(this_eot.reveal.draw_importence_num, this_eot.reveal.others_num,
            this_eot.reveal.give_paper_num, this_eot.reveal.nothing_num)
        if reveal_num == this_eot.reveal.draw_importence_num:
            reveal_message = u'通过划重点'
        elif reveal_num == this_eot.reveal.give_paper_num:
            reveal_message = u"通过给‘模拟题’"
        elif reveal_num == this_eot.reveal.nothing_num:
            reveal_message = u'不透题或透题非常不给力'
        else:
            reveal_message = u'其他给力透题方式或无需透题'
        
        usual_work_num = compare_3(this_eot.usual_work.less_num, 
            this_eot.usual_work.some_num, this_eot.usual_work.more_num)
        num_all = this_eot.usual_work.less_num+this_eot.usual_work.some_num+this_eot.usual_work.more_num
        if usual_work_num == this_eot.usual_work.less_num:
            percent = float(this_eot.usual_work.less_num) / num_all
            usual_work_message = u'很少或没有（%.0f%%）'% (percent*100)
        elif usual_work_num == this_eot.usual_work.some_num:
            percent = float(this_eot.usual_work.some_num) / num_all
            usual_work_message = u'有一些或适当的作业（%.0f%%）'% (percent*100)
        else:
            percent = float(this_eot.usual_work.more_num) / num_all
            usual_work_message = u'较多或非常多（%.0f%%）'% (percent*100)
            
        comments = this_eot.comment_set.all()
        after_range_num = 5        
        befor_range_num = 4       
        try:                     
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(comments,5)   
        try:                     
            comments_list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            comments_list = paginator.page(paginator.num_pages)
        if page >= after_range_num:
            page_range = paginator.page_range[page-after_range_num:page+befor_range_num]
        else:
            page_range = paginator.page_range[0:int(page)+befor_range_num]
        comments = comments_list
        
        
        if not comments:
            comments_message = u'暂时没有人评论此课程'
        else:
            comments_message = False
        
        luckies = First_3.objects.filter(eot=this_eot, lucky=1)
        if not luckies:
            luckies_message = False
        else:
            luckies_message = True
            
        lucky_message = random.choice([
            u'在前100位评价此课程的人中，这些人幸运地被历史铭记',
            u'感谢这些人率先评价了此课程',
            u'历史意外地记住了这些评价此课程的先驱']
            )
    
        this_teacher = this_eot.teacher
        this_course = this_eot.course
        sameteacher = Eot.objects.filter(teacher = this_eot.teacher,
            university = this_eot.university).exclude(id=this_eot.id)

        if not sameteacher:
            message_sameteacher = u'抱歉，暂时没有发现相关的数据'
    
        samecourse = Eot.objects.filter(course = this_eot.course,
            university = this_eot.university).exclude(id=this_eot.id)
        
        if not samecourse:
            message_samecourse = u'抱歉，暂时没有发现相关的数据'  
        
        datas = Eot_data.objects.filter(eot=this_eot)
        
        imgs = Eot_img.objects.filter(eot=this_eot)
        
        score_string = this_eot.score_list
        score_list = score_string.split(';')
        for index, item in enumerate(score_list):
            score_list[index] = int(item)

        max_num = max(score_list)
        
        steps = (max_num/5+1)* 5
        
        if request.user.is_authenticated():
            user = request.user
            try: 
                this_user_info = User_info.objects.get(user=user)
                if this_user_info.store_eot:       
                    storeEot_list = this_user_info.store_eot.split(';')[:-1]
                    if u'%s' % this_eot.id in storeEot_list:
                        store_message = True
                    else:
                        store_message = False
                else:
                    store_message = False
            except:
                 this_user_info = User_info(
                    store_eot = '',
                    download_Eotdata = '',
                    nocomment_Eotdata = '',
                    grade = u'公民',
                    user = user
                 )
                 this_user_info.save()
                 store_message = False
        
    else:
        store_message = False
        datas = False
        if credit_id == '':
            this_teacher = u'此老师'
            this_course = u'此课程'
            message_sameteacher = u'抱歉，暂时没有发现相关的数据'
            message_samecourse = u'抱歉，暂时没有发现相关的数据'
        else:      
            credit = Credit.objects.get(id=credit_id)
            university_info = University_info.objects.get(id=credit.university_info_id)
            sameteacher = Eot.objects.filter(
                teacher = credit.course_teacher,
                university = university_info.school
            )
            if credit.course_teacher == '':
                this_teacher = '本课'
            else:
                this_teacher = '%s' % credit.course_teacher
            this_course = credit.course_name
            if not sameteacher:
                message_sameteacher = u'抱歉，暂时没有发现相关的数据'
        
            samecourse = Eot.objects.filter(
                course = credit.course_name,
                university = university_info.school
            )
            
            if not samecourse:
                message_samecourse = u'抱歉，暂时没有发现相关的数据'       
            
            
    if kwargs:
        try:
            lucky = kwargs['lucky']
            money_message = kwargs['money_message']
        except:
            pass
    
    #last_url = request.GET.get('Referer')
    if kwargs: 
        try:
            fileForm = kwargs['fileForm']
        except:
            fileForm = Eot_dataForm()
    else:
        fileForm = Eot_dataForm()
        
    if kwargs: 
        try:
            imgForm = kwargs['imgForm']
        except:
            imgForm = Eot_imgForm()
    else:
        imgForm = Eot_imgForm()
    
    try:
        can = request.META['HTTP_REFERER']
        try:
            last_url = request.session['last_url']
            path = 'http://' + request.META['HTTP_HOST'] + request.path
            if request.META['HTTP_REFERER'] != path:
                if '/eot/showcredit/' in request.META['HTTP_REFERER'] and '/eot/showeot/' in request.path:
                    pass
                elif '/eot/showcomment/' in request.META['HTTP_REFERER'] and '/eot/showcredit/' in request.path:
                    request.session['last_url'] = '/index/'
                    last_url = request.session['last_url']
                elif '/eot/showcomment/' in request.META['HTTP_REFERER'] and '/eot/showeot/' in request.path:
                    request.session['last_url'] = '/list/'
                    last_url = request.session['last_url']
                else:    
                    request.session['last_url'] = request.META['HTTP_REFERER']
                    last_url = request.session['last_url']       
        except:
            request.session['last_url'] = request.META['HTTP_REFERER']
            last_url = request.session['last_url']
    except:
        pass
    
    
    return render_to_response('show.html',locals(),
        context_instance=RequestContext(request))
     
def showcredit(request, credit_id):     
    credit = Credit.objects.get(id=credit_id)
    university_info = University_info.objects.get(id=credit.university_info_id)
    try:
        this_eot = Eot.objects.get(
            course = credit.course_name,
            teacher = credit.course_teacher,
            university = university_info.school
        )
        no_eot = False
    except:
        no_eot = True
        this_eot = None   
    return show(request,this_eot,no_eot,credit_id)
 
def showeot(request, eot_id,**kwargs):
    if kwargs:
        lucky = kwargs['lucky']
        money_message = kwargs['money_message']
    try:
        this_eot = Eot.objects.get(id=eot_id)
        no_eot = False
    except:
        no_eot = True
        this_eot = None
    credit_id = ''
    if kwargs:
        return show(request,this_eot,no_eot, credit_id,lucky=lucky,money_message=money_message)
    else:
        return show(request,this_eot,no_eot, credit_id)

@login_required(login_url='/log/')
def value(request, credit_id):
    if request.method == 'GET':
        user = request.user
        credit = Credit.objects.get(id=credit_id)
        if credit.course_teacher == '':           
            cannot_message = True
            no_teacher_message = True
            return render_to_response('value.html',locals(),
                context_instance=RequestContext(request))
        elif credit.course_attr == '':
            cannot_message = True
            no_attr_message = True
            return render_to_response('value.html',locals(),
                context_instance=RequestContext(request))
        else:
            return render_to_response('value.html',locals(),
                context_instance=RequestContext(request))
    elif request.method == 'POST':
        lists = ['course_score','teacher_score', 'like_or_hate','naming','naming_way',
            'atmosphere','teach_way','popularity','mid_test','mid_test_way',
            'usual_work','final_test_way','final_test_degree','reveal','if_dead']
        for list in lists:
            if not list in request.POST:
                value_wrong_message = u'存在未填项，请填写完整后再提交！'
                credit = Credit.objects.get(id=credit_id)
                return render_to_response('value.html',locals(),
                    context_instance=RequestContext(request)) 
        user = request.user
        university_info = University_info.objects.get(id=user.university_info_id)
        credit = Credit.objects.get(id=credit_id)
        try:
            teacher_info = Teacher.objects.get(university=university_info.school, 
                name=credit.course_teacher)
            num = teacher_info.value_num
            teacher_info.avg_score = (teacher_info.avg_score * num + 
                float(request.POST.get('teacher_score'))) / (num+1)            
        except:
            teacher_info = Teacher(
                university = university_info.school,
                name = credit.course_teacher,
                value_num = 1,
                avg_score = float(request.POST.get('teacher_score'))
            )
        finally:
            teacher_info.save()
            
        try:
            this_eot = Eot.objects.get(
                course = credit.course_name,
                teacher = credit.course_teacher,
                university = university_info.school
            )
            
            if this_eot.college == u'选修学院':
                if credit.course_attr == u'必修':
                    this_eot.college = university_info.college
            
            value_num = this_eot.value_num
            
            list_string = this_eot.score_list
            list = list_string.split(';')
            index = judge_score(credit.course_score)
            list[index] = '%s' % (int(list[index])+1)
            list_string = ';'.join(list)
            this_eot.score_list = list_string
            
            
            
            this_eot.value_num = value_num + 1
            
            this_eot.course_avg_score = (this_eot.course_avg_score * value_num + 
                float(request.POST.get('course_score'))) / (value_num+1)
                
            this_eot.teacher_avg_score = (this_eot.teacher_avg_score * value_num + 
                float(request.POST.get('teacher_score'))) / (value_num+1)
            
            this_eot.history_avg_score = (this_eot.history_avg_score * value_num + 
                float(credit.course_score)) / (value_num+1)
                
            if request.POST.get('like_or_hate') == 'like':
                this_eot.like_num += 1
            elif request.POST.get('like_or_hate') == 'hate':
                this_eot.hate_num += 1
            else:
                this_eot.middle_num += 1
                
            naming_choose = request.POST.get('naming')
            if naming_choose == 'never_num':
                this_eot.naming.never_num += 1
            elif naming_choose == 'sometimes_num':
                this_eot.naming.sometimes_num += 1
            else:
                this_eot.naming.often_num += 1
            this_eot.naming.save()
            
            naming_way_choose = request.POST.get('naming_way')
            if naming_way_choose == 'no_num':
                this_eot.naming_way.no_num += 1
            elif naming_way_choose == 'sign_num':
                this_eot.naming_way.sign_num += 1
            elif naming_way_choose == 'answer_num':
                this_eot.naming_way.answer_num += 1
            else:
                this_eot.naming_way.hybrid_num += 1
            this_eot.naming_way.save()
            
            atmosphere_choose = request.POST.get('atmosphere')
            if atmosphere_choose == 'dead_num':
                this_eot.atmosphere.dead_num += 1
            elif atmosphere_choose == 'normal_num':
                this_eot.atmosphere.normal_num += 1
            else:
                this_eot.atmosphere.active_num += 1
            this_eot.atmosphere.save()
            
            teach_way_choose = request.POST.get('teach_way')
            if teach_way_choose == 'PPT_num':
                this_eot.teach_way.PPT_num += 1
            elif teach_way_choose == 'book_num':
                this_eot.teach_way.book_num += 1
            elif teach_way_choose == 'teacher_num':
                this_eot.teach_way.teacher_num += 1
            else:
                this_eot.teach_way.hybrid_num += 1
            this_eot.teach_way.save()
            
            popularity_choose = request.POST.get('popularity')
            if popularity_choose == 'most_num':
                this_eot.popularity.most_num += 1                  
            elif popularity_choose == 'more_num':
                this_eot.popularity.more_num += 1
            elif popularity_choose == 'less_num':
                this_eot.popularity.less_num += 1
            else:
                this_eot.popularity.nobody_num += 1
            this_eot.popularity.save()
            
            mid_test_choose = request.POST.get('mid_test')
            if mid_test_choose == 'yes_num':
                this_eot.mid_test.yes_num += 1
            else:
                this_eot.mid_test.no_num += 1
            this_eot.mid_test.save()
            
            mid_test_way_choose = request.POST.get('mid_test_way')
            if mid_test_way_choose == 'no_num':
                this_eot.mid_test_way.no_num += 1
            elif mid_test_way_choose == 'paper_num':
                this_eot.mid_test_way.paper_num += 1
            elif mid_test_way_choose == 'open_num':
                this_eot.mid_test_way.open_num += 1
            elif mid_test_way_choose == 'pravite_num':
                this_eot.mid_test_way.pravite_num += 1
            else:
                this_eot.mid_test_way.inspect_num += 1
            this_eot.mid_test_way.save()
            
            dead_choose = request.POST.get('if_dead')
            if dead_choose == 'yes':
                this_eot.dead_num += 1
            
            final_test_way_choose = request.POST.get('final_test_way')
            if final_test_way_choose == 'paper_num':
                this_eot.final_test_way.paper_num += 1
            elif final_test_way_choose == 'open_num':
                this_eot.final_test_way.open_num += 1
            elif final_test_way_choose == 'pravite_num':
                this_eot.final_test_way.pravite_num += 1
            else:
                this_eot.final_test_way.inspect_num += 1
            this_eot.final_test_way.save()
            
            final_test_degree_choose = request.POST.get('final_test_degree')
            this_eot.final_test_degree += int(final_test_degree_choose)
            
            reveal_choose = request.POST.get('reveal')
            if reveal_choose == 'draw_importence_num':
                this_eot.reveal.draw_importence_num += 1
            elif reveal_choose == 'give_paper_num':
                this_eot.reveal.give_paper_num += 1
            elif reveal_choose == 'others_num':
                this_eot.reveal.others_num += 1
            else:
                this_eot.reveal.nothing_num += 1
            this_eot.reveal.save()
            
            usual_work_choose = request.POST.get('usual_work')
            if usual_work_choose == 'less_num':
                this_eot.usual_work.less_num += 1
            elif usual_work_choose == 'some_num':
                this_eot.usual_work.some_num += 1
            else:
                this_eot.usual_work.more_num += 1
            this_eot.usual_work.save()
            
            if user.money >= 5:
                if request.POST.get('recommend_num') == None:
                    recommend = 0
                else:
                    recommend = 1
                    user.money += 5
                    user.save()
                this_eot.recommend_num += recommend
            
            
            this_eot.save()         
                
        except Eot.DoesNotExist:
            if request.POST.get('like_or_hate') == 'like':
                like = 1
                hate = 0
                middle = 0
            elif request.POST.get('like_or_hate') == 'hate':
                hate = 1
                like = 0
                middle = 0
            else:
                hate = 0
                like = 0
                middle = 1
            if user.money >= 5:
                if request.POST.get('recommend_num') == None:
                    recommend = 0
                else:
                    recommend = 1
                    user.money -= 5
                    user.save()
            else:
                recommend = 0
            naming_choose = request.POST.get('naming')
            if naming_choose == 'never_num':
                this_Eot_naming = Eot_naming(
                    never_num = 1,
                    sometimes_num = 0,
                    often_num = 0
                )
            elif naming_choose == 'sometimes_num':
                this_Eot_naming = Eot_naming(
                    never_num = 0,
                    sometimes_num = 1,
                    often_num = 0
                )
            else:
                this_Eot_naming = Eot_naming(
                    never_num = 0,
                    sometimes_num = 0,
                    often_num = 1
                )
            this_Eot_naming.save()
            
            naming_way_choose = request.POST.get('naming_way')
            if naming_way_choose == 'no_num':
                this_Eot_naming_way = Eot_naming_way(
                    no_num = 1,
                    sign_num = 0,
                    answer_num = 0,
                    hybrid_num = 0
                )
            elif naming_way_choose == 'sign_num':
                this_Eot_naming_way = Eot_naming_way(
                    no_num = 0,
                    sign_num = 1,
                    answer_num = 0,
                    hybrid_num = 0
                )
            elif naming_way_choose == 'answer_num':
                this_Eot_naming_way = Eot_naming_way(
                    no_num = 0,
                    sign_num = 0,
                    answer_num = 1,
                    hybrid_num = 0
                )
            else:
                this_Eot_naming_way = Eot_naming_way(
                    no_num = 0,
                    sign_num = 0,
                    answer_num = 0,
                    hybrid_num = 1 
                )
            this_Eot_naming_way.save()    
            atmosphere_choose = request.POST.get('atmosphere')
            if atmosphere_choose == 'dead_num':
                this_Eot_atmosphere = Eot_atmosphere(
                    dead_num = 1,
                    normal_num = 0,
                    active_num = 0
                )
            elif atmosphere_choose == 'normal_num':
                this_Eot_atmosphere = Eot_atmosphere(
                    dead_num = 0,
                    normal_num = 1,
                    active_num = 0
                )
            else:
                this_Eot_atmosphere = Eot_atmosphere(
                    dead_num = 0,
                    normal_num = 0,
                    active_num = 1
                )
            this_Eot_atmosphere.save()    
            teach_way_choose = request.POST.get('teach_way')
            if teach_way_choose == 'PPT_num':
                this_Eot_teach_way = Eot_teach_way(
                    PPT_num = 1,
                    book_num = 0,
                    teacher_num = 0,
                    hybrid_num = 0
                )
            elif teach_way_choose == 'book_num':
                this_Eot_teach_way = Eot_teach_way(
                    PPT_num = 0,
                    book_num = 1,
                    teacher_num = 0,
                    hybrid_num = 0
                )
            elif teach_way_choose == 'teacher_num':
                this_Eot_teach_way = Eot_teach_way(
                    PPT_num = 0,
                    book_num = 0,
                    teacher_num = 1,
                    hybrid_num = 0
                )
            else:
                this_Eot_teach_way = Eot_teach_way(
                    PPT_num = 0,
                    book_num = 0,
                    teacher_num = 0,
                    hybrid_num = 1
                )
            this_Eot_teach_way.save()    
            popularity_choose = request.POST.get('popularity')
            if popularity_choose == 'most_num':
                this_Eot_popularity = Eot_popularity(
                    most_num = 1,
                    more_num = 0,
                    less_num = 0,
                    nobody_num = 0
                )                  
            elif popularity_choose == 'more_num':
                this_Eot_popularity = Eot_popularity(
                    most_num = 0,
                    more_num = 1,
                    less_num = 0,
                    nobody_num = 0
                )
            elif popularity_choose == 'less_num':
                this_Eot_popularity = Eot_popularity(
                    most_num = 0,
                    more_num = 0,
                    less_num = 1,
                    nobody_num = 0
                )
            else:
                this_Eot_popularity = Eot_popularity(
                    most_num = 0,
                    more_num = 0,
                    less_num = 0,
                    nobody_num = 1
                )
            this_Eot_popularity.save()
            mid_test_choose = request.POST.get('mid_test')
            if mid_test_choose == 'yes_num':
                this_Eot_mid_test = Eot_mid_test(
                    yes_num = 1,
                    no_num = 0
                )
            else:
                this_Eot_mid_test = Eot_mid_test(
                    yes_num = 0,
                    no_num = 1
                )
            this_Eot_mid_test.save()
            mid_test_way_choose = request.POST.get('mid_test_way')
            if mid_test_way_choose == 'no_num':
                this_Eot_mid_test_way = Eot_mid_test_way(
                    no_num = 1,
                    paper_num = 0,
                    open_num = 0,
                    pravite_num = 0,
                    inspect_num = 0
                )
            elif mid_test_way_choose == 'paper_num':
                this_Eot_mid_test_way = Eot_mid_test_way(
                    no_num = 0,
                    paper_num = 1,
                    open_num = 0,
                    pravite_num = 0,
                    inspect_num = 0
                )
            elif mid_test_way_choose == 'open_num':
                this_Eot_mid_test_way = Eot_mid_test_way(
                    no_num = 0,
                    paper_num = 0,
                    open_num = 1,
                    pravite_num = 0,
                    inspect_num = 0
                )
            elif mid_test_way_choose == 'pravite_num':
                this_Eot_mid_test_way = Eot_mid_test_way(
                    no_num = 0,
                    paper_num = 0,
                    open_num = 0,
                    pravite_num = 1,
                    inspect_num = 0
                )
            else:
                this_Eot_mid_test_way = Eot_mid_test_way(
                    no_num = 0,
                    paper_num = 0,
                    open_num = 0,
                    pravite_num = 0,
                    inspect_num = 1
                )
            this_Eot_mid_test_way.save()    
            final_test_way_choose = request.POST.get('final_test_way')
            if final_test_way_choose == 'paper_num':
                this_Eot_final_test_way = Eot_final_test_way(
                    paper_num = 1,
                    open_num = 0,
                    pravite_num = 0,
                    inspect_num =0
                )
            elif final_test_way_choose == 'open_num':
                this_Eot_final_test_way = Eot_final_test_way(
                    paper_num = 0,
                    open_num = 1,
                    pravite_num = 0,
                    inspect_num =0
                )
            elif final_test_way_choose == 'pravite_num':
                this_Eot_final_test_way = Eot_final_test_way(
                    paper_num = 0,
                    open_num = 0,
                    pravite_num = 1,
                    inspect_num =0
                )
            else:
                this_Eot_final_test_way = Eot_final_test_way(
                    paper_num = 0,
                    open_num = 0,
                    pravite_num = 0,
                    inspect_num =1
                )
            this_Eot_final_test_way.save()
            
            reveal_choose = request.POST.get('reveal')
            if reveal_choose == 'draw_importence_num':
                this_Eot_reveal = Eot_reveal(
                    draw_importence_num = 1,
                    give_paper_num = 0,
                    nothing_num = 0,
                    others_num = 0
                )
            elif reveal_choose == 'give_paper_num':
                this_Eot_reveal = Eot_reveal(
                    draw_importence_num = 0,
                    give_paper_num = 1,
                    nothing_num = 0,
                    others_num = 0
                )
            elif reveal_choose == 'others_num':
                this_Eot_reveal = Eot_reveal(
                    draw_importence_num = 0,
                    give_paper_num = 0,
                    nothing_num = 0,
                    others_num = 1
                )
            else:
                this_Eot_reveal = Eot_reveal(
                    draw_importence_num = 0,
                    give_paper_num = 0,
                    nothing_num = 1,
                    others_num = 0
                )
            this_Eot_reveal.save()
            usual_work_choose = request.POST.get('usual_work')
            if usual_work_choose == 'less_num':
                this_Eot_usual_work = Eot_usual_work(
                    less_num = 1,
                    some_num = 0,
                    more_num = 0
                )
            elif usual_work_choose == 'some_num':
                this_Eot_usual_work = Eot_usual_work(
                    less_num = 0,
                    some_num = 1,
                    more_num = 0
                )
            else:
                this_Eot_usual_work = Eot_usual_work(
                    less_num = 0,
                    some_num = 0,
                    more_num = 1
                )
            this_Eot_usual_work.save() 
            if credit.course_attr == u'必修':
                this_college = university_info.college
            else:
                this_college = u'选修学院'
            
            dead_choose = request.POST.get('if_dead')
            if dead_choose == 'yes':
                this_dead_num = 1
            else:
                this_dead_num = 0
            this_eot = Eot(
                course = credit.course_name,
                teacher = credit.course_teacher,
                university = university_info.school,
                college = this_college,
                value_num = 1,
                course_avg_score = float(request.POST.get('course_score')),
                teacher_avg_score = teacher_info.avg_score,
                history_avg_score = credit.course_score,
                credit = credit.course_credit,
                like_num = like,
                hate_num = hate,
                middle_num = middle,
                recommend_num = recommend,
                dead_num = this_dead_num,
                score_list = '0;0;0;0;0;0;0;0;0;0',
                
                naming = this_Eot_naming,
                naming_way = this_Eot_naming_way,
                atmosphere = this_Eot_atmosphere,
                teach_way = this_Eot_teach_way,
                popularity = this_Eot_popularity,
                
                mid_test = this_Eot_mid_test,
                mid_test_way = this_Eot_mid_test_way,
                final_test_way = this_Eot_final_test_way,
                final_test_degree = request.POST.get('final_test_degree'),
                reveal = this_Eot_reveal,
                usual_work = this_Eot_usual_work,
            )
            this_eot.save()
            
            list_string = this_eot.score_list
            list = list_string.split(';')
            index = judge_score(credit.course_score)
            list[index] = '%s' % (int(list[index])+1)
            list_string = ';'.join(list)
            this_eot.score_list = list_string
            this_eot.save()
                

        comment_choose = request.POST.get('comment')
        if comment_choose =='':
            pass
        else:
            this_Eot_comment = Eot_comment(
                user = user,
                comment = comment_choose,
                agree_num = 0,
                disagree_num = 0,
                eot = this_eot
            )
            this_Eot_comment.save()
            
        
        if First_3.objects.filter(eot=this_eot).count() < 100:
            if First_3.objects.filter(eot=this_eot,lucky=1).count() < 10:
                choice = random.randrange(1,100,1)
                if choice < 10:
                    lucky = 1
                    user.first_value += 1
                else:
                    lucky = 0
                first_3 = First_3(
                    user = user,
                    lucky = lucky,
                    eot = this_eot
                )
                first_3.save()
            else:
                lucky = 0
        else:
            lucky = 0
        money = random.randrange(1,11,1)
        credit.add_money = 10 + money
        credit.save()
        user.money = user.money + credit.add_money
        user.save()
        money_message = credit.add_money
        return showeot(request, this_eot.id, lucky=lucky,money_message=money_message)

@login_required(login_url='/log/')        
def list(request):
    user = request.user
    university_info = University_info.objects.get(id=user.university_info_id)
    credits = Credit.objects.filter(user=user)
    if not credits:
        message_majorcourse = u'抱歉，暂时没有发现相关的数据'
    else:
        #course_list = []
        #for credit in credits:
            #course_list.append(credit.course_name)
        major_eot = Eot.objects.filter(university = university_info.school).order_by('course','-course_avg_score')
        major_eot_after_range_num = 5        
        major_eot_befor_range_num = 4       
        try:                     
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(major_eot,12)   
        try:                     
            major_eot_list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            major_eot_list = paginator.page(paginator.num_pages)
        if page >= major_eot_after_range_num:
            major_eot_page_range = paginator.page_range[page-major_eot_after_range_num:page+major_eot_befor_range_num]
        else:
            major_eot_page_range = paginator.page_range[0:int(page)+major_eot_befor_range_num]
        major_eot = major_eot_list
        if not major_eot:
            message_majorcourse = u'抱歉，暂时没有发现相关的数据'
        
    recommend_collegecourse = Eot.objects.filter(
        university=university_info.school).exclude(recommend_num=0).order_by('-recommend_num')
    recommend_collegecourse_after_range_num = 5        
    recommend_collegecourse_befor_range_num = 4       
    try:                     
        page = int(request.GET.get("page",1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    paginator = Paginator(recommend_collegecourse,12)   
    try:                     
        recommend_collegecourse_list = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        recommend_collegecourse_list = paginator.page(paginator.num_pages)
    if page >= recommend_collegecourse_after_range_num:
        recommend_collegecourse_page_range = paginator.page_range[page-recommend_collegecourse_after_range_num:page+recommend_collegecourse_befor_range_num]
    else:
        recommend_collegecourse_page_range = paginator.page_range[0:int(page)+recommend_collegecourse_befor_range_num]
    recommend_collegecourse = recommend_collegecourse_list
    if not recommend_collegecourse:
        message_collegerecomend = u'抱歉，暂时没有发现相关的数据'
    
    highhistory = Eot.objects.filter(university=university_info.school).order_by('-history_avg_score')
    if not highhistory:
        message_highhistory = u'抱歉，暂时没有发现相关的数据'
    else:
        if highhistory.count() > 9:
            highhistory = highhistory[:10]
    
    highteacher = Teacher.objects.filter(university=university_info.school).order_by('-avg_score')
    if not highteacher:
        message_highteacher = u'抱歉，暂时没有发现相关的数据'
    else:
        if highteacher.count() > 9:
            highteacher = highteacher[:10]
            
    highcourse = Eot.objects.filter(university=university_info.school).order_by('-course_avg_score')
    if not highcourse:
        message_highcourse = u'抱歉，暂时没有发现相关的数据'
    else:
        if highcourse.count() > 9:
            highcourse = highcourse[:10]
    
    xuankeHTML = True
    return render_to_response('list.html',locals(),
        context_instance=RequestContext(request)) 

@csrf_exempt
@login_required(login_url='/log/')       
def poll(request):
    if request.is_ajax() and request.method == 'POST':
        if 'poll_info' in request.POST:
            id, num = request.POST.get('poll_info').split('-')
            id=int(id)
            try:
                this_comment = Eot_comment.objects.get(id=id)
                user = request.user
                if this_comment.user == user:
                    response = HttpResponse()
                    return response
                else:
                    if num == '1':
                        this_comment.agree_num += 1
                    else:
                        this_comment.disagree_num += 1
                    this_comment.save()
                    response = HttpResponse()
                    return response
            except:
                response = HttpResponse()
                return response

@login_required(login_url='/log/')                
def search(request):
    if request.is_ajax() and request.method == 'GET':
        if 'search' in request.GET:
            user = request.user
            university_info = University_info.objects.get(id=user.university_info_id)
            items = request.GET.get('search').split(';')
            for index,text in enumerate(items):
                 items[index] = text.strip()               
            if items[0] == 'course':
                answer = Eot.objects.filter(
                     university = university_info.school,
                     course__icontains=items[1],
                     course_avg_score__gte = items[2],
                     teacher_avg_score__gte = items[3],
                     history_avg_score__gte = items[4]
                )
                if not answer:
                    return render_to_response('search_nothing.html',locals(),
                        context_instance=RequestContext(request))
            elif items[0] == 'teacher':
                answer = Eot.objects.filter(
                    university = university_info.school,
                    teacher__icontains=items[1],
                    course_avg_score__gte = items[2],
                    teacher_avg_score__gte = items[3],
                    history_avg_score__gte = items[4]
                )
                if not answer:
                    return render_to_response('search_nothing.html',locals(),
                        context_instance=RequestContext(request))
            elif items[0] == 'major':
                this_university_info = University_info.objects.filter(
                    school = university_info.school,
                    major__icontains = items[1]
                )
                if not this_university_info:
                    return render_to_response('search_nothing.html',locals(),
                        context_instance=RequestContext(request))
                else:
                    major_coursename = Major_course.objects.filter(
                        major_id = this_university_info[0].id
                    )
                    if not major_coursename:
                        return render_to_response('search_nothing.html',locals(),
                            context_instance=RequestContext(request))
                    else:
                        names = []
                        teachers = []
                        for course in major_coursename:
                            names.append(course.course_name)
                            teachers.append(course.course_teacher)
                        answer = Eot.objects.filter(
                            course__in=(names), 
                            teacher__in=(teachers),                        
                            university = university_info.school,
                            course_avg_score__gte = items[2],
                            teacher_avg_score__gte = items[3],
                            history_avg_score__gte = items[4]
                        )
                        if not answer:
                            return render_to_response('search_nothing.html',locals(),
                                context_instance=RequestContext(request))
            else:
                answer = Eot.objects.filter(                  
                    university = university_info.school,
                    college = university_info.college
                )
                if not answer:
                    return render_to_response('search_nothing.html',locals(),
                        context_instance=RequestContext(request))
            if 'no' in items:
                for eot in answer:
                    if eot.mid_test.yes_num >= eot.mid_test.no_num:
                        answer = answer.exclude(id=eot.id)
                if not answer:
                    return render_to_response('search_nothing.html',locals(),
                        context_instance=RequestContext(request))
            if 'nohard' in items:
                for eot in answer:
                    if eot.final_test_degree.hard_num > (eot.value_num/2):
                        answer = answer.exclude(id=eot.id)
                if not answer:
                    return render_to_response('search_nothing.html',locals(),
                        context_instance=RequestContext(request))
            if 'nooften' in items:
                for eot in answer:
                    if eot.naming.often_num > (eot.value_num/2):
                        answer = answer.exclude(id=eot.id)
                if not answer:
                    return render_to_response('search_nothing.html',locals(),
                        context_instance=RequestContext(request)) 
            if 'nomore' in items:
                for eot in answer:
                    if eot.usual_work.more_num > (eot.value_num/2):
                        answer = answer.exclude(id=eot.id)
                if not answer:
                    return render_to_response('search_nothing.html',locals(),
                        context_instance=RequestContext(request))
            answer = answer.order_by('-course_avg_score')
            num = answer.count()
            return render_to_response('search_answer.html',locals(),
                context_instance=RequestContext(request)) 

@login_required(login_url='/log/')                  
def search_sort(request):
    if request.is_ajax() and request.method == 'GET':
        if 'sort' in request.GET:
            ids = request.GET.get('ids')
            ids_list = ids.split(';')[:-1]
            sort = request.GET.get('sort')            
            if sort == 'coursescore':               
                sort_message = u'课程评分'              
                answer = Eot.objects.filter(id__in=ids_list).order_by('-course_avg_score')
                return render_to_response('search_sort_course.html',locals(),
                    context_instance=RequestContext(request))
            elif sort == 'teacherscore':
                sort_message = u'教师评分'
                answer = Eot.objects.filter(id__in=ids_list).order_by('-teacher_avg_score')
                return render_to_response('search_sort_teacher.html',locals(),
                    context_instance=RequestContext(request))
            elif sort == 'qimoscore':
                sort_message = u'期末平均分'
                answer = Eot.objects.filter(id__in=ids_list).order_by('-history_avg_score')
                return render_to_response('search_sort_qimo.html',locals(),
                    context_instance=RequestContext(request))
            elif sort == 'recommendnum':
                sort_message = u'推荐人数'
                answer = Eot.objects.filter(id__in=ids_list).order_by('-recommend_num')
                return render_to_response('search_sort_recommend.html',locals(),
                    context_instance=RequestContext(request))
            else:
                sort_message = u'点赞人数'
                answer = Eot.objects.filter(id__in=ids_list).order_by('-like_num')
            return render_to_response('search_sort_like.html',locals(),
                context_instance=RequestContext(request)) 

@login_required(login_url='/log/')                
def uploadfile(request,eot_id):
    if request.method == 'POST':
        form = Eot_dataForm(request.POST,request.FILES)
        if form.is_valid():
            data = Eot_data(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                warning_num = 0,
                download_num =  0,
                price_num =  form.cleaned_data['price_num'],
                #upload_time =  
                owner = request.user,
                eot = Eot.objects.get(id=eot_id),
                file = form.cleaned_data['file'],
                profit = 0
            )
            data.save()
            eot = Eot.objects.get(id=eot_id)
            eot.save()
            return HttpResponseRedirect('/eot/showeot/%s/' % eot_id)
        else:
            no_eot = False
            credit_id = ''
            this_eot = Eot.objects.get(id=eot_id)
            return show(request,this_eot,no_eot, credit_id,fileForm=form)

@login_required(login_url='/log/')            
def downloadfile(request,data_id,path):    
    temp = tempfile.TemporaryFile() 
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED) 
    src = settings.MEDIA_ROOT  
    filename = path.split('/')[1]
    zipname = filename.split('.')[1]
    archive.write(src+'/'+path, filename) 
    archive.close() 
    wrapper = FileWrapper(temp) 
    response = HttpResponse(wrapper, content_type='application/zip') 
    response['Content-Disposition'] = 'attachment; filename=%s.zip' % zipname
    response['Content-Length'] = temp.tell() 
    temp.seek(0)
    user = request.user
    data = Eot_data.objects.get(id=data_id)
    
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
        
    if not data_id in this_user_info.download_Eotdata:
        this_user_info.download_Eotdata += '%s;' % data_id
    if not data_id in this_user_info.nocomment_Eotdata:
        this_user_info.nocomment_Eotdata += '%s;' % data_id
    this_user_info.save()
    
    if user.money > data.price_num:
        user.money  -= data.price_num
    else:
        user.money = 0
    user.save()
    
    now = datetime.date.today()
    if (now - data.upload_time).days < 180:
        data.owner.money += data.price_num
        data.owner.save()
        data.profit += data.price_num
        data.save()
    data.download_num += 1
    data.save()
    return response

@login_required(login_url='/log/')                
def uploadImg(request,eot_id):
    if request.method == 'POST':
        form = Eot_imgForm(request.POST,request.FILES)
        if form.is_valid():
            img = Eot_img(
                title = form.cleaned_data['title'],
                description = form.cleaned_data['description'],
                owner = request.user,
                eot = Eot.objects.get(id=eot_id),
                img = form.cleaned_data['img'],
                like_num = 0,
                if_safe = '0'
            )
            img.save()
            eot = Eot.objects.get(id=eot_id)
            eot.save()
            return HttpResponseRedirect('/eot/showeot/%s/' % eot_id)
        else:
            no_eot = False
            credit_id = ''
            this_eot = Eot.objects.get(id=eot_id)
            return show(request,this_eot,no_eot, credit_id,imgForm=form)    
       
def showcomment(request,Eotdata_id):
    user = request.user
    this_Eotdata = Eot_data.objects.get(id=Eotdata_id)
    if user.is_authenticated():
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
        
        if this_user_info.nocomment_Eotdata:
            nocomment_list = this_user_info.nocomment_Eotdata.split(';')[:-1]
            if Eotdata_id in nocomment_list:
                can_comment = True
            else:
                can_comment = False
        else:
            can_comment = False
        
    comments = Eotdata_comment.objects.filter(eot_data=this_Eotdata)
    if not comments:
        comments = None
    else:
        comments_after_range_num = 5        
        comments_befor_range_num = 4       
        try:                     
            page = int(request.GET.get("page",1))
            if page < 1:
                page = 1
        except ValueError:
            page = 1
        paginator = Paginator(comments,12)   
        try:                     
            comments_list = paginator.page(page)
        except(EmptyPage,InvalidPage,PageNotAnInteger):
            comments_list = paginator.page(paginator.num_pages)
        if page >= comments_after_range_num:
            comments_page_range = paginator.page_range[page-comments_after_range_num:page+comments_befor_range_num]
        else:
            comments_page_range = paginator.page_range[0:int(page)+comments_befor_range_num]
        comments = comments_list
    
    try:
        can = request.META['HTTP_REFERER']
        try:
            last_url = request.session['last_url']

            path = 'http://' + request.META['HTTP_HOST'] + request.path
            if request.META['HTTP_REFERER'] != path:
                request.session['last_url'] = request.META['HTTP_REFERER']
                last_url = request.session['last_url']
        except:
            request.session['last_url'] = request.META['HTTP_REFERER']
            last_url = request.session['last_url']
    except:
        pass
    
    try:
        this_Report_eotData = Report_eotData.objects.get(eot_data=this_Eotdata)
        condition = this_Report_eotData.result
    except:
        condition = 'no'
    return render_to_response('showcomment.html',locals(),
        context_instance=RequestContext(request))

@login_required(login_url='/log/')        
def comment_Eotdata(request,Eotdata_id):
    user = request.user
    this_Eotdata = Eot_data.objects.get(id=Eotdata_id)
    this_Eotdata_comment = Eotdata_comment(
        user = user,
        comment = request.POST.get('comment'),
        eot_data = this_Eotdata
    )
    this_Eotdata_comment.save()
    this_Eotdata.save()
    nocomment_list = user.nocomment_Eotdata.split(';')[:-1]
    nocomment_list.remove('%s' % Eotdata_id)
    if nocomment_list:
        s = ';'.join(nocomment_list)
        user.nocomment_Eotdata = s + ';'
    else:
        user.nocomment_Eotdata = ''
    user.save()
    return HttpResponseRedirect('/eot/showcomment/%s' % Eotdata_id)

@csrf_exempt
@login_required(login_url='/log/') 
def store_eot(request):
    if request.is_ajax() and request.method == 'GET':
        if 'eot_id' in request.GET:
            id = request.GET.get('eot_id')
            user = request.user
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
            this_user_info.store_eot += '%s;' % id
            this_user_info.save()
            return render_to_response('store_eot.html',locals(),
                context_instance=RequestContext(request))
 
@csrf_exempt
@login_required(login_url='/log/')  
def delStore(request):
    if request.is_ajax() and request.method == 'GET':
        if 'eot_id' in request.GET:
            id = request.GET.get('eot_id')
            user = request.user
            this_user_info = User_info.objects.get(user=user)
            storeEot_list = this_user_info.store_eot.split(';')[:-1]
            storeEot_list.remove('%s' % id)
            if storeEot_list:
                s = ';'.join(storeEot_list)
                this_user_info.store_eot = s + ';'
            else:
                this_user_info.store_eot = ''
            this_user_info.save()
            return render_to_response('delStore.html',locals(),
                context_instance=RequestContext(request))
    
def test(request):
    user = request.user
    if request.POST.get('recommend_num') == None:
        recommend = 0
    else:
        recommend = 1
    return render_to_response('wrong.html',locals(),
        context_instance=RequestContext(request)) 
#coding:utf-8

from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.conf import settings
from EOT.models import *
from University.models import University_info
from Center.models import User_info
from Affair.models import Report_eotData
from account.models import MyUser
from django.core.urlresolvers import reverse 
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage  
from django.core.mail import send_mail, EmailMultiAlternatives
import os
import time
import datetime 
import threading

from_email = settings.EMAIL_HOST_USER

class EmailThread(threading.Thread):

    def __init__(self, subject, text_content, from_email, recipient_list, fail_silently, html_content):
        self.subject = subject
        self.text_content = text_content
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html_content = html_content
        threading.Thread.__init__(self)

    def run(self):
        msg = EmailMultiAlternatives(self.subject, self.text_content, self.from_email, self.recipient_list)
        if self.html_content:
            msg.attach_alternative(self.html_content, 'text/html')
        msg.send(self.fail_silently)

def send_mail(subject, text_content, from_email, recipient_list, fail_silently=False, html_content=None, *args, **kwargs):
    EmailThread(subject, text_content, from_email, recipient_list, fail_silently, html_content).start()


@login_required(login_url='/log/')
def report_eotData(request):
    if request.is_ajax() and request.method == 'GET':
        if 'info' in request.GET:
            print request.GET.get('info')
            eot_id,this_Eotdata_id,owner_id = request.GET.get('info').split(';')
            this_Eot_data = Eot_data.objects.get(id=this_Eotdata_id)
            this_eot = Eot.objects.get(id=eot_id)
            this_owner = MyUser.objects.get(id=owner_id)
            this_reporter = request.user
            this_Report_eotData = Report_eotData(
                eot = this_eot,
                eot_data = this_Eot_data,
                suspect = this_owner,
                reporter = request.user,
                result = '0'
            )
            this_Report_eotData.save()
            
            print '1'
            
            subject = u'大学易管理员提醒'
            text_content = u'用户举报课程资料'
            recipient_list = ['you_xiang_123@sina.com',]
            this_html = loader.render_to_string('remindReport_admin.html',
                {'affairUrl':'http://127.0.0.1:8000/affair/',
                    'remindMessage':u'有用户举报了课程资料'}
                    
                
            )
            send_mail(subject, text_content, from_email, recipient_list, html_content=this_html)
            
            print '2'
            
            subject = u'大学易举报机制提醒'
            text_content = u'您上传课程资料被举报'
            recipient_list = [this_owner.email,]
            user_nic_name = request.user.nic_name
            course_name = this_eot.course
            data_name = this_Eot_data.title
            data_url = 'http://127.0.0.1:8000/eot/showeot/%s/' % this_eot.id
            this_html = loader.render_to_string('remindReport_suspect.html',{
                'user_nic_name':user_nic_name,
                'course_name':course_name,
                'data_name':data_name,
                'data_url':data_url
                }
            )
            send_mail(subject, text_content, from_email, recipient_list, html_content=this_html)
            
            print '3'
            
            text_content = u'您举报了课程资料'
            recipient_list = [request.user.email,]
            user_nic_name = request.user.nic_name
            this_html = loader.render_to_string('remindReport_reporter.html', {
                'user_nic_name':user_nic_name,
                'course_name':course_name,
                'data_name':data_name,
                'data_url':data_url
                }
            )
            send_mail(subject, text_content, from_email, recipient_list, html_content=this_html)           
            
            print '4'
            email = request.user.email
            return render_to_response('report_eotData_success.html',locals(),
                context_instance=RequestContext(request))
        else:
            return render_to_response('report_eotData_fail.html',locals(),
                context_instance=RequestContext(request))
    else:
        return render_to_response('report_eotData_fail.html',locals(),
                context_instance=RequestContext(request))

@login_required(login_url='/log/')
def report_eotImg(request,Report_eotImg_id):
    this_Eot_img = Eot_img.objects.get(id=Report_eotImg_id)
    this_Eot_img.if_safe = '-1'
    this_Eot_img.save()
    
    subject = u'大学易管理员提醒'
    text_content = u'用户举报课程图片'
    recipient_list = ['you_xiang_123@sina.com',]
    this_html = loader.render_to_string('remindReport_admin.html',
        {'affairUrl':'http://127.0.0.1:8000/affair/',
         'remindMessage':u'有用户举报了课程图片'}
    )
    send_mail(subject, text_content, from_email, recipient_list, html_content=this_html)
    
    refreshTime = '5'
    next = request.META['HTTP_REFERER']
    moreMessage = u'感谢您支持大学易，我们已经收到了您的举报并将尽快处理！'
    refreshMessage = u'Loading……5s后跳转回上一页面，请稍候'
    return render_to_response('nextPage.html',locals(),
        context_instance=RequestContext(request))
                
@login_required(login_url='/log/') 
def affair(request):
    if request.user.is_admin:
        notSolved_Report_eotDatas = Report_eotData.objects.filter(result='0').order_by('-report_time')
        if notSolved_Report_eotDatas:
            notSolved_Report_eotDatas_after_range_num = 5        
            notSolved_Report_eotDatas_befor_range_num = 4       
            try:                     
                page = int(request.GET.get("page",1))
                if page < 1:
                    page = 1
            except ValueError:
                page = 1
            paginator = Paginator(notSolved_Report_eotDatas,12)   
            try:                     
                notSolved_Report_eotDatas_list = paginator.page(page)
            except(EmptyPage,InvalidPage,PageNotAnInteger):
                notSolved_Report_eotDatas_list = paginator.page(paginator.num_pages)
            if page >= notSolved_Report_eotDatas_after_range_num:
                notSolved_Report_eotDatas_page_range = paginator.page_range[page-notSolved_Report_eotDatas_after_range_num:page+notSolved_Report_eotDatas_befor_range_num]
            else:
                notSolved_Report_eotDatas_page_range = paginator.page_range[0:int(page)+notSolved_Report_eotDatas_befor_range_num]
            notSolved_Report_eotDatas = notSolved_Report_eotDatas_list
        else:
           notSolved_Report_eotDatas = None
           
        Solved_Report_eotDatas = Report_eotData.objects.all().exclude(result='0').order_by('result','reporter','-report_time')
        if Solved_Report_eotDatas:
            Solved_Report_eotDatas_after_range_num = 5        
            Solved_Report_eotDatas_befor_range_num = 4       
            try:                     
                page = int(request.GET.get("page",1))
                if page < 1:
                    page = 1
            except ValueError:
                page = 1
            paginator = Paginator(Solved_Report_eotDatas,12)   
            try:                     
                Solved_Report_eotDatas_list = paginator.page(page)
            except(EmptyPage,InvalidPage,PageNotAnInteger):
                Solved_Report_eotDatas_list = paginator.page(paginator.num_pages)
            if page >= Solved_Report_eotDatas_after_range_num:
                Solved_Report_eotDatas_page_range = paginator.page_range[page-Solved_Report_eotDatas_after_range_num:page+Solved_Report_eotDatas_befor_range_num]
            else:
                Solved_Report_eotDatas_page_range = paginator.page_range[0:int(page)+Solved_Report_eotDatas_befor_range_num]
            Solved_Report_eotDatas = Solved_Report_eotDatas_list
        else:
            Solved_Report_eotDatas = None
            
        notSolved_eotImg = Eot_img.objects.filter(if_safe='-1')
        return render_to_response('affair.html',locals(),
            context_instance=RequestContext(request))
    else:
        return render_to_response('illegal.html',locals(),
            context_instance=RequestContext(request))

@login_required(login_url='/log/')             
def handle_reportEotData_dispose(request, eotData_id, dispose):
    if request.user.is_admin:
        this_Report_eotData = Report_eotData.objects.get(id=Report_eotData_id)
        if dispose == '-1':
            this_Report_eotData.result = '-1'
            this_Report_eotData.solve_time = datetime.date.today()
            this_Report_eotData.save()
            
            course_name = this_Report_eotData.eot.course
            data_name = this_Report_eotData.eot_data.title
            data_url = 'http://127.0.0.1:8000/eot/showeot/%s/' % this_Report_eotData.eot.id
            
            subject = u'大学易举报机制提醒'
            text_content = u'您的举报未通过审核'
            recipient_list = [this_Report_eotData.reporter.email,]
            user_nic_name = this_Report_eotData.reporter.nic_name            
            this_html = loader.render_to_string('reportFail_reporter.html', {
                'user_nic_name':user_nic_name,
                'course_name':course_name,
                'data_name':data_name,
                'data_url':data_url
                }
            )
            send_mail(subject, text_content, from_email, recipient_list, html_content=this_html)
            
            text_content = u'您的课程资料已通过审核'
            recipient_list = [this_Report_eotData.suspect.email,]
            user_nic_name = this_Report_eotData.suspect.nic_name
            this_html = loader.render_to_string('reportFail_suspect.html', {
                'user_nic_name':user_nic_name,
                'course_name':course_name,
                'data_name':data_name,
                'data_url':data_url
                }
            )
            send_mail(subject, text_content, from_email, recipient_list, html_content=this_html)
            
            return HttpResponseRedirect('/affair/')
        if dispose == '1':       
            old_file = settings.MEDIA_ROOT + '/' + str(this_Report_eotData.eot_data.file)
            old_profit = this_Report_eotData.eot_data.profit
            this_Report_eotData.suspect.money -= old_profit
            this_Report_eotData.suspect.save()
            this_data = this_Report_eotData.eot_data
            this_Report_eotData.result = '1'
            this_Report_eotData.solve_time = datetime.date.today()
            this_Report_eotData.save()
            this_data.delete()
            if os.path.isfile(old_file):
                os.remove(old_file)
            
            subject = u'大学易举报机制提醒'
            course_name = this_Report_eotData.eot.course
            data_name = u'已被删除'
            data_url = 'http://127.0.0.1:8000/eot/showeot/%s/' % this_Report_eotData.eot.id
            
            text_content = u'您的举报已通过审核'
            recipient_list = [this_Report_eotData.reporter.email,]
            user_nic_name = this_Report_eotData.reporter.nic_name            
            this_html = loader.render_to_string('reportSuccess_reporter.html', {
                'user_nic_name':user_nic_name,
                'course_name':course_name,
                'data_name':data_name,
                'data_url':data_url
                }
            )
            send_mail(subject, text_content, from_email, recipient_list, html_content=this_html)
            
            text_content = u'您的课程资料未通过审核'
            recipient_list = [this_Report_eotData.suspect.email,]
            user_nic_name = this_Report_eotData.suspect.nic_name
            this_html = loader.render_to_string('reportSuccess_suspect.html', {
                'user_nic_name':user_nic_name,
                'course_name':course_name,
                'data_name':data_name,
                'data_url':data_url
                }
            )
            send_mail(subject, text_content, from_email, recipient_list, html_content=this_html)
            
            return HttpResponseRedirect('/affair/')
    else:
        return render_to_response('illegal.html',locals(),
            context_instance=RequestContext(request))

def handle_reportEotImg_dispose(request, eotImg_id, dispose):
    this_eotImg = Eot_img.objects.get(id=eotImg_id)
    if dispose == '-1':
        this_eotImg.if_safe = '1'
        this_eotImg.save()
        return HttpResponseRedirect('/affair/')
    if dispose == '1':
        old_file = settings.MEDIA_ROOT + '/' + str(this_eotImg.img)
        print settings.MEDIA_ROOT
        print str(this_eotImg.img)
        this_eotImg.delete()
        print old_file
        if os.path.isfile(old_file):
            os.remove(old_file)
            print 'delete img successfully'
        return HttpResponseRedirect('/affair/')


def test_sendEmail2(request):
    subject, from_email, to = 'hello', 'collegeyi@sina.com', 'you_xiang_123@sina.com'
    text_content = u'这是一封重要的邮件'
    html_content = u'<b>激活链接：</b><a href="http://www.baidu.com">http:www.baidu.com</a>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    return render_to_response('sendEmail_successful.html',locals(),
        context_instance=RequestContext(request)) 
        
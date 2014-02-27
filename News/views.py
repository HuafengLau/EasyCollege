#coding:utf-8
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import PageNotAnInteger, Paginator, InvalidPage, EmptyPage
from django.conf import settings

def news(request):
    return HttpResponseRedirect('/news/all/all/')
    
def which_news(request,news_interest,news_part):
    newsHTML = True
    return render_to_response('news.html',locals(),
        context_instance=RequestContext(request))
        
        
    
        
        
            
                 
    


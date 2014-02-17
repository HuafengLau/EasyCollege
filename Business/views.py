#encoding:utf-8

import chardet 
import bs4
from bs4 import BeautifulSoup
import codecs
import urllib
import urllib2
import cookielib
from django.shortcuts import render_to_response
from django.template import RequestContext
from University.models import University_info

def guide_getCreditFile(request,school_code):
    upper_code = school_code.upper()
    if school_code == 'ecnu':
        name = u'*艺真同学'
    if school_code == 'gnnu':
        name = u'*佑鹏同学'
    if school_code == 'imnu':
        name = u'*纪尧同学'
    if school_code == 'nwsuaf':
        name = u'*隆堂同学'
    if school_code == 'bistu':
        name = u'*元庆同学'
    if school_code == 'xcc':
        name = u'*盈盈同学'
    if school_code == 'xhu':
        name = u'*思梦同学'
    if school_code == 'dlmedu':
        name = u'*渊博同学'
    if school_code == 'hbue':
        name = u'*婧'
    if school_code == 'hunnu':
        name = u'*传贵'
    if school_code == 'scut':
        name = u'*晓凤'
    if school_code == 'jxufe':
        name = u'*咪同学'
        more = True 
        return render_to_response('CFileGuideJxufe.html',locals(),
            context_instance=RequestContext(request))
    if school_code == 'ncu':
        name = u'*健民同学'
        more = True 
        return render_to_response('CFileGuideNcu.html',locals(),
            context_instance=RequestContext(request))        
    if school_code == 'nenu':
        name = u'*秀红同学'
        more = True 
        return render_to_response('CFileGuideNenu.html',locals(),
            context_instance=RequestContext(request))
    
    more_school = ['nwsuaf',]
    if school_code in more_school:
        more = True
     
    return render_to_response('CFileGuideBase.html',locals(),
        context_instance=RequestContext(request))        

def get_soup(doc):
    doc_encoding = chardet.detect(doc)['encoding']
    soup = BeautifulSoup(''.join(doc), from_encoding=doc_encoding)
    return soup

def get_doc(login_page,url,zh, mm):
    cj = cookielib.CookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        
    data = urllib.urlencode({"zjh":zh,"mm":mm})
        
    request = urllib2.Request(login_page, data)
    request.add_header('User=Agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0')
    response = opener.open(request)
  
    next = opener.open(url)
    doc = next.read()
    return doc
    
def get_url(login_page,url,zh, mm):
    doc = get_doc(login_page,url,zh, mm)
    soup = get_soup(doc)
    href = soup.findAll('a', target="lnfaIfra")[0]
    if 'http://jwcxk.aufe.edu.cn/' in url:
        return 'http://jwcxk.aufe.edu.cn/' + href['href']
    if 'http://202.115.47.141/' in url:
        return 'http://202.115.47.141/' + href['href']
        

def str_change(str):
    return str.strip()

def GPA(user,zh,mm):
    university_info_id = user.university_info_id
    school = University_info.objects.get(id=university_info_id).school
    if school == u'安徽财经大学':
        login_page = 'http://jwcxk.aufe.edu.cn/loginAction.do'
        url = 'http://jwcxk.aufe.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
    if school == u'四川大学':
        login_page = 'http://202.115.47.141/loginAction.do'
        url = 'http://202.115.47.141/gradeLnAllAction.do?type=ln&oper=fa'
    url = get_url(login_page,url,zh, mm)
    doc = get_doc(login_page,url,zh, mm)
    soup = get_soup(doc)
    TRS = soup.findAll('tr', attrs={"class" : "odd"})
    courses=[]
    for index, item in enumerate(TRS):
        course = []
        TR = TRS[index].contents
        course.append(str_change(TR[5].contents[0]))
        course.append(str_change(TR[9].contents[0]))
        course.append(str_change(TR[11].contents[0]))
        course.append(str_change(TR[13].contents[1].contents[0]))
        courses.append(course)
    print len(courses)
    return courses  
    
def ecnu(doc):
    points = []
    soup = get_soup(doc)
    try:
        all_a = soup.findAll('a',{'href':'javascript:void(0)'})
        for a in all_a:
            point = []
            this_name = a.contents[0]
            this_attr = a.parent.findNextSiblings('td')[0].string
            this_credit = a.parent.findNextSiblings('td')[1].string
            this_score = a.parent.findNextSiblings('td')[2].string
            point.append(str_change(this_name))
            point.append(str_change(this_credit))
            point.append(str_change(this_attr))
            point.append(str_change(this_score))
            points.append(point)
        return points
    except:
        return None

def gnnu(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.findAll('table',{'class':'datelist'})[0]
        TRs = table.findAll('tr')
        for index, TR in enumerate(TRs):
            point = []
            if index == 0:
                continue
            else:
                tds = TR.findAll('td')           
                name = str_change(tds[3].string)
                attr = str_change(tds[4].string)
                credit = str_change(tds[6].string)
                score = str_change(tds[8].string)
                point.append(name)
                point.append(credit)
                point.append(attr)
                point.append(score)
                points.append(point)           
        return points
    except:
        return None

def imnu(doc):
    points = []
    soup = get_soup(doc)
    try:
        TRS = soup.findAll('tr', attrs={"class" : "odd"})
        courses=[]
        for index, item in enumerate(TRS):
            course = []
            TR = TRS[index].contents
            course.append(str_change(TR[5].contents[0]))
            course.append(str_change(TR[9].contents[0]))
            course.append(str_change(TR[11].contents[0]))
            course.append(str_change(TR[13].contents[1].contents[0]))
            courses.append(course)

        return courses 
    except:
        return None

def nwsuaf(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.find('table', attrs={"class" : "datalist"})
        TRs = table.findAll('tr')
        for index, TR in enumerate(TRs):
            if index == 0:
                continue
            else:
                point = []
                tds = TR.findAll('td')
                try:
                    name = str_change(tds[3].string)
                    score = str_change(tds[10].string)
                    credit = str_change(tds[11].string)
                    attr = str_change(tds[14].string)
                    point.append(name)
                    point.append(credit)
                    point.append(attr)
                    point.append(score)
                    
                    points.append(point)
                except:
                    continue           
        return points
    except:
        return None

def bistu(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.findAll('table',{'class':'datelist'})[0]
        TRs = table.findAll('tr')
        for index, TR in enumerate(TRs):
            point = []
            if index == 0:
                continue
            else:
                tds = TR.findAll('td')           
                name = str_change(tds[1].string)
                attr = str_change(tds[2].string)
                score = str_change(tds[4].string)
                credit = str_change(tds[8].string)           
                point.append(name)
                point.append(credit)
                point.append(attr)
                point.append(score)           
                points.append(point)  
        return points
    except:
        return None

def jxufe(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.find('table',{'style':'border:1px solid #CCCCCC;padding:5px;background:#F3F3F3 ;line-height : normal ;border-collapse:collapse;'})
        tbody = table.find('tbody')
        TRs = tbody.findAll('tr')
        for index, TR in enumerate(TRs):  
            point = []
            tds = TR.findAll('td')
            name = str_change(tds[1].string)
            attr = ''
            score = str_change(tds[9].string)
            credit = str_change(tds[7].string)
            teacher = str_change(tds[3].string)
            
            if teacher == 'getTeacherName': 
                continue
            else:
                point.append(name)
                point.append(credit)
                point.append(attr)
                point.append(score)
                point.append(teacher)
                points.append(point)
        return points
    except:
        return None

def xcc(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.findAll('table',{'class':'datelist'})[0]
        TRs = table.findAll('tr')
        for index, TR in enumerate(TRs):
            point = []
            if index == 0:
                continue
            else:
                tds = TR.findAll('td')           
                name = str_change(tds[3].string)
                sttr = str_change(tds[4].string)
                credit = str_change(tds[6].string)
                score = str_change(tds[8].string)
                point.append(name)
                point.append(credit)
                point.append(sttr)
                point.append(score)

                points.append(point)
        return points
    except:
        return None

def xhu(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.findAll('table',{'class':'datelist'})[0]
        TRs = table.findAll('tr')
        for index, TR in enumerate(TRs):
            point = []
            if index == 0:
                continue
            else:
                tds = TR.findAll('td')           
                name = str_change(tds[3].string)
                sttr = str_change(tds[4].string)
                credit = str_change(tds[6].string)
                score = str_change(tds[8].string)
                point.append(name)
                point.append(credit)
                point.append(sttr)
                point.append(score)

                points.append(point)
        return points
    except:
        return None

def dlmedu(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.findAll('table',{'class':'datelist'})[0]
        TRs = table.findAll('tr')
        for index, TR in enumerate(TRs):
            point = []
            if index == 0:
                continue
            else:
                tds = TR.findAll('td')           
                name = str_change(tds[3].string)
                sttr = str_change(tds[4].string)
                credit = str_change(tds[6].string)
                score = str_change(tds[8].string)
                point.append(name)
                point.append(credit)
                point.append(sttr)
                point.append(score)

                points.append(point)
        return points
    except:
        return None

def hbue(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.findAll('table',{'class':'datelist'})[0]
        TRs = table.findAll('tr')
        for index, TR in enumerate(TRs):
            point = []
            if index == 0:
                continue
            else:
                tds = TR.findAll('td')           
                name = str_change(tds[3].string)
                sttr = str_change(tds[4].string)
                credit = str_change(tds[6].string)
                score = str_change(tds[12].string)
                point.append(name)
                point.append(credit)
                point.append(sttr)
                point.append(score)

                points.append(point)  
        return points
    except:
        return None

def nenu(doc):
    points = []
    soup = get_soup(doc)
    try:
        TRs = soup.findAll('tr',{'class':"smartTr"})
        for TR in TRs:
            point = []
            tds = TR.findAll('td')
              
            name = str_change(tds[4].string)
            attr = ''
            credit = str_change(tds[10].string)
            score = str_change(tds[5].string)
            point.append(name)
            point.append(credit)
            point.append(attr)
            point.append(score)
            
            points.append(point)
        return points
    except:
        return None

def hunnu(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.findAll('table',{'class':'datelist'})[0]
        TRs = table.findAll('tr')
        for index, TR in enumerate(TRs):
            point = []
            if index == 0:
                continue
            else:
                tds = TR.findAll('td')           
                name = str_change(tds[3].string)
                attr = str_change(tds[4].string)
                credit = str_change(tds[6].string)
                score = str_change(tds[8].string)
                point.append(name)
                point.append(credit)
                point.append(attr)
                point.append(score)

                points.append(point)
        return points
    except:
        return None

def scut(doc):
    points = []
    soup = get_soup(doc)
    try:
        table = soup.findAll('table',{'class':'datelist'})[0]
        TRs = table.findAll('tr')
        for index, TR in enumerate(TRs):
            point = []
            if index == 0:
                continue
            else:
                tds = TR.findAll('td')           
                name = str_change(tds[3].string)
                sttr = str_change(tds[4].string)
                credit = str_change(tds[6].string)
                score = str_change(tds[8].string)
                point.append(name)
                point.append(credit)
                point.append(sttr)
                point.append(score)

                points.append(point)
        return points
    except:
        return None
        
def wise_analyzeCreditFile(doc,school_code):
    if school_code == 'ecnu':
        points = ecnu(doc)
    if school_code == 'gnnu':
        points = gnnu(doc)
    if school_code == 'imnu':
        points = imnu(doc)
    if school_code == 'nwsuaf':
        points = nwsuaf(doc)
    if school_code == 'bistu':
        points = bistu(doc) 
    if school_code == 'jxufe':
        points = jxufe(doc)
    if school_code == 'xcc':
        points = xcc(doc)
    if school_code == 'xhu':
        points  = xhu(doc)
    if school_code == 'dlmedu':
        points = dlmedu(doc)
    if school_code == 'hbue':
        points = hbue(doc)
    if school_code == 'nenu':
        points = nenu(doc)
    if school_code == 'hunnu':
        points = hunnu(doc)
    if school_code == 'scut':
        points = scut(doc)
    return points
    

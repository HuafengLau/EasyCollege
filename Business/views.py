#encoding:utf-8

import chardet 
import bs4
from bs4 import BeautifulSoup
import codecs
import urllib
import urllib2
import cookielib
        

def get_soup(doc):
    doc_encoding = chardet.detect(doc)['encoding']
    soup = BeautifulSoup(''.join(doc), from_encoding=doc_encoding)
    return soup

def get_doc(url,user, password):
    login_page = 'http://202.115.47.141/loginAction.do'
    cj = cookielib.CookieJar();
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        
    data = urllib.urlencode({"zjh":user,"mm":password})
        
    request = urllib2.Request(login_page, data)
    request.add_header('User=Agent', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0')
    response = opener.open(request)
  
    next = opener.open(url)
    doc = next.read()
    return doc
    
def get_url(user, password):
    url = 'http://202.115.47.141/gradeLnAllAction.do?type=ln&oper=fa'
    doc = get_doc(url,user, password)
    soup = get_soup(doc)
    href = soup.findAll('a', target="lnfaIfra")[0]
    return 'http://202.115.47.141/' + href['href']
        

def str_change(str):
    return str.strip()

def GPA(user, password):
    url = get_url(user, password)
    doc = get_doc(url,user, password)
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
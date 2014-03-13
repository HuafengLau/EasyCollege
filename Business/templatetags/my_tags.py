#coding:utf-8

from django import template
from University.models import University_info
from EOT.models import Eot, Eot_data, Eot_data
from Business.models import Credit
from Business.views import code_school
from datetime import datetime
import re
import pytz

register = template.Library()

@register.tag 
def ifintInstr(parser, token): 
    return do_ifintInstr(parser, token, False) 
 
@register.tag 
def ifnotintInstr(parser, token): 
    return do_ifintInstr(parser, token, True) 
 
 
def do_ifintInstr(parser, token, negate): 
    bits = list(token.split_contents()) 
    if len(bits) != 3: 
        raise TemplateSyntaxError("%r takes two arguments" % bits[0]) 
    end_tag = 'end' + bits[0] 
    nodelist_true = parser.parse(('else', end_tag)) 
    token = parser.next_token() 
    if token.contents == 'else': 
        nodelist_false = parser.parse((end_tag,)) 
        parser.delete_first_token() 
    else: 
        nodelist_false = NodeList() 
    val1 = parser.compile_filter(bits[1]) 
    val2 = parser.compile_filter(bits[2]) 
    return IfintInstrNode(val1, val2, nodelist_true, nodelist_false, negate) 
 
 
class IfintInstrNode(template.Node): 
    child_nodelists = ('nodelist_true', 'nodelist_false') 
 
    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate): 
        self.var1, self.var2 = var1, var2 
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false 
        self.negate = negate 
 
    def __repr__(self): 
        return "<IfEqualNode>" 
 
    def render(self, context): 
        val1 = self.var1.resolve(context, True) 
        val2 = self.var2.resolve(context, True) 
        if (self.negate and str(val1) not in val2) or (not self.negate and str(val1) in val2): 
            return self.nodelist_true.render(context) 
        return self.nodelist_false.render(context) 

        
class ShowCourseNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        values = self.sequence.resolve(context, True) 
        if '(' in values:
            text1, text2 = values.split('(')
            text2 = '('+ text2
            return '%s<br>%s' % (text1, text2)
        else:
            return ''
        
def ShowCourse(parser, token):
    try:
        tag_name, text_name= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(text_name)    
    return ShowCourseNode(sequence)

class ShowSchoolNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        values = self.sequence.resolve(context, True) 
        try:
            this_University_info = University_info.objects.get(id=values)
            name = this_University_info.school
            return '%s' % name
        except:
            return 'wrong id'
        
def ShowSchool(parser, token):
    try:
        tag_name, text_name= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(text_name)    
    return ShowSchoolNode(sequence)
    
class RobotNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        #values = self.sequence.resolve(context, True)
        if str(self.sequence) == 'credit':
            credits = Credit.objects.all()
            s = ''
            for credit in credits:
                s += 'Allow: /eot/showcredit/%s/\r\n' % credit.id
            return s
        elif str(self.sequence) == 'eot':
            eots = Eot.objects.all()
            s = ''
            for eot in eots:
                s += 'Allow: /eot/showeot/%s/\r\n' % eot.id
            return s
        elif str(self.sequence) == 'eotcomment':
            eotdatas = Eot_data.objects.all()
            s = ''
            for eotdata in eotdatas:
                s += 'Allow: /eot/showcomment/%s/\r\n' % eotdata.id
            return s
        elif str(self.sequence) == 'getCreditFile':
            s = ''
            for (k,v) in  code_school.items():          
                s += 'Allow: /business/guide/getCreditFile/%s/\r\n' % k
            return s
        else:
            return 'wrong Robot thing'
            
def Robot(parser, token):
    try:
        tag_name, text_name= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(text_name)    
    return RobotNode(sequence)

class SitemapNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        #values = self.sequence.resolve(context, True)
        if str(self.sequence) == 'today': 
            now = datetime.now()
            if now.month < 10:
                month = '0%s' % now.month
            else:
                month = now.month
            if now.day < 10:
                day = '0%s' % now.day
            else:
                day = now.day
            return '%s-%s-%s' % (now.year,month,day)
        elif str(self.sequence) == 'showcredit':    
            credits = Credit.objects.all()
            s = ''
            for credit in credits:
                try:
                    this_eot = Eot.objects.get(
                        course = credit.course_name,
                        teacher = credit.course_teacher,
                        university = university_info.school
                    )
                    if eot.last_modified:
                        lastmod = this_eot.last_modified
                    else:
                        this_eot.save()
                        lastmod = this_eot.last_modified
                except:
                    lastmod = credit.add_date
                s_temp1 = '\r\n   <url>\r\n\r\n      <loc>http://www.collegeyi.com/eot/showcredit/%s/</loc>\r\n' % credit.id
                s_temp2 = '\r\n      <lastmod>%s</lastmod>\r\n' % lastmod
                s_temp3 = '\r\n      <changefreq>weekly</changefreq>\r\n\r\n   </url>\r\n'
                s += s_temp1 + s_temp2 + s_temp3
            return s
        elif str(self.sequence) == 'showeot': 
            eots = Eot.objects.all()
            s = ''
            for eot in eots:
                if eot.last_modified:
                    lastmod = eot.last_modified
                else:
                    eot.save()
                    lastmod = eot.last_modified
                s_temp1 = '\r\n   <url>\r\n\r\n      <loc>http://www.collegeyi.com/eot/showeot/%s/</loc>\r\n' % eot.id
                s_temp2 = '\r\n      <lastmod>%s</lastmod>\r\n' % lastmod
                s_temp3 = '\r\n      <changefreq>weekly</changefreq>\r\n\r\n   </url>\r\n'
                s += s_temp1 + s_temp2 + s_temp3
            return s
        elif str(self.sequence) == 'eotcomment':
            eotdatas = Eot_data.objects.all()
            s = ''
            for eotdata in eotdatas:
                if eotdata.last_modified:
                    lastmod = eotdata.last_modified
                else:
                    eotdata.save()
                    lastmod = eotdata.last_modified
                s_temp1 = '\r\n   <url>\r\n\r\n      <loc>http://www.collegeyi.com/eot/showcomment/%s/</loc>\r\n' % eotdata.id
                s_temp2 = '\r\n      <lastmod>%s</lastmod>\r\n' % lastmod
                s_temp3 = '\r\n      <changefreq>weekly</changefreq>\r\n\r\n   </url>\r\n'
                s += s_temp1 + s_temp2 + s_temp3
            return s
        elif str(self.sequence) == 'getCreditFile':
            s = ''
            school_time = '2014-02-24'
            for (k,v) in  code_school.items(): 
                s_temp1 = '\r\n   <url>\r\n\r\n      <loc>http://www.collegeyi.com/business/guide/getCreditFile/%s/</loc>\r\n' % k
                s_temp2 = '\r\n      <lastmod>%s</lastmod>\r\n' % school_time
                s_temp3 = '\r\n      <changefreq>yearly</changefreq>\r\n\r\n   </url>\r\n'
                s += s_temp1 + s_temp2 + s_temp3
            return s
        else:
            return 'wrong Robot thing'
            
def Sitemap(parser, token):
    try:
        tag_name, text_name= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(text_name)    
    return SitemapNode(sequence)

class showNewsTimeNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        values = self.sequence.resolve(context, True)

        #tz = pytz.timezone(pytz.country_timezones('cn')[0])  
        #now2 = tz.localize(datetime.now())
        now1 = datetime.now(pytz.utc)
        #now = datetime.now()
        time1 = (now1 - values.time).total_seconds()
        #time2 = (now2 - values.time).total_seconds()
        if time1 >= 86400:
            num = int(time1 / 86400)
            return '%s 天' % num
        elif time1 >= 3600:
            num = int(time1 / 3600)
            return '%s 小时' % num
        elif time1 >= 60:
            num = int(time1 / 60)
            return '%s 分钟' % num
        else:
            num = int(time1)
            return '%s 秒' % num
            
def showNewsTime(parser, token):
    try:
        tag_name, text_name= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(text_name)    
    return showNewsTimeNode(sequence)

class newsScoreClassNode(template.Node):
    def __init__(self,sequence1,sequence2):
        self.sequence1 = sequence1
        self.sequence2 = sequence2

    def render(self, context):
        info = self.sequence1.resolve(context, True)
        news = self.sequence2.resolve(context, True)
        if news.score >=0:
            if news.score > 100:
                size = '3'
            elif news.score >10:
                size ='2'
            else:
                size = '1'
        else:
            if abs(news.score) > 100:
                size = '-3'
            elif abs(news.score) >10:
                size ='-2'
            else:
                size = '-1'
            
        vote = 'unVoteNum'
        if info.upVoted_news and str(news.id) in info.upVoted_news:
            vote = 'VotedNum'
        if info.downVoted_news and str(news.id) in info.downVoted_news:
            vote = 'VotedNum'
            
        s = vote + size
        return s
            
def newsScoreClass(parser, token):
    try:
        tag_name, info, news= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence1 = parser.compile_filter(info)
    sequence2 = parser.compile_filter(news)
    
    return newsScoreClassNode(sequence1,sequence2)  
  
register.tag('ShowCourse', ShowCourse)
register.tag('ShowSchool', ShowSchool)
register.tag('Robot', Robot)
register.tag('Sitemap', Sitemap)
register.tag('showNewsTime', showNewsTime)
register.tag('newsScoreClass', newsScoreClass)
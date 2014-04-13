#coding:utf-8

from django import template
from University.models import University_info
from EOT.models import Eot, Eot_data, Eot_data
from Business.models import Credit
from Business.views import code_school
from datetime import datetime
import re
import pytz
from News.models import NewsPart,News
from account.models import MyUser
from University.models import University_info
from Center.models import User_info

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

@register.tag 
def ifVoted(parser, token): 
    return do_ifVoted(parser, token, False) 
 
@register.tag 
def ifnotVoted(parser, token): 
    return do_ifVoted(parser, token, True) 
 
 
def do_ifVoted(parser, token, negate): 
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
    return IfVotedNode(val1, val2, nodelist_true, nodelist_false, negate) 
 
 
class IfVotedNode(template.Node): 
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
        this_user_info = User_info.objects.get(user=val2)
        judge = False
        if this_user_info.upVoted_news and str(val1.id) in this_user_info.upVoted_news:
            judge = True
        if this_user_info.downVoted_news and str(val1.id) in this_user_info.downVoted_news:
            judge = True 
        if val1.user == val2:
            judge = True
        if (self.negate and not judge) or (not self.negate and judge): 
            return self.nodelist_true.render(context) 
        return self.nodelist_false.render(context)         
 
@register.tag 
def ifCommentVoted(parser, token): 
    return do_ifCommentVoted(parser, token, False) 
 
@register.tag 
def ifnotCommentVoted(parser, token): 
    return do_ifCommentVoted(parser, token, True) 
 
 
def do_ifCommentVoted(parser, token, negate): 
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
    return IfCommentVotedNode(val1, val2, nodelist_true, nodelist_false, negate) 
 
 
class IfCommentVotedNode(template.Node): 
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
        this_user_info = User_info.objects.get(user=val2)
        judge = False
        try:
            news = val1.news
            if this_user_info.upVoted_comment1 and str(val1.id) in this_user_info.upVoted_comment1:
                judge = True
            if this_user_info.downVoted_comment1 and str(val1.id) in this_user_info.downVoted_comment1:
                judge = True 
            if val1.user == val2:
                judge = True
        except:
            try:
                newscomment1 = val1.newscomment1
                if this_user_info.upVoted_comment2 and str(val1.id) in this_user_info.upVoted_comment2:
                    judge = True
                if this_user_info.downVoted_comment2 and str(val1.id) in this_user_info.downVoted_comment2:
                    judge = True 
                if val1.user == val2:
                    judge = True
            except:
                try:
                    newscomment2 = val1.newscomment2
                    if this_user_info.upVoted_comment3 and str(val1.id) in this_user_info.upVoted_comment3:
                        judge = True
                    if this_user_info.downVoted_comment3 and str(val1.id) in this_user_info.downVoted_comment3:
                        judge = True 
                    if val1.user == val2:
                        judge = True
                except:
                    try:
                        newscomment3 = val1.newscomment3
                        if this_user_info.upVoted_comment4 and str(val1.id) in this_user_info.upVoted_comment4:
                            judge = True
                        if this_user_info.downVoted_comment4 and str(val1.id) in this_user_info.downVoted_comment4:
                            judge = True 
                        if val1.user == val2:
                            judge = True
                    except:
                        judge = False
        if (self.negate and not judge) or (not self.negate and judge): 
            return self.nodelist_true.render(context) 
        return self.nodelist_false.render(context)  
 
@register.tag 
def judgeStudent(parser, token): 
    return do_judgeStudent(parser, token, False) 
 
@register.tag 
def judgenotStudent(parser, token): 
    return do_judgeStudent(parser, token, True) 
 
 
def do_judgeStudent(parser, token, negate): 
    bits = list(token.split_contents()) 
    if len(bits) != 2: 
        raise TemplateSyntaxError("%r takes one arguments" % bits[0]) 
    end_tag = 'end' + bits[0] 
    nodelist_true = parser.parse(('else', end_tag)) 
    token = parser.next_token() 
    if token.contents == 'else': 
        nodelist_false = parser.parse((end_tag,)) 
        parser.delete_first_token() 
    else: 
        nodelist_false = NodeList() 
    val1 = parser.compile_filter(bits[1]) 
    return do_judgeStudentNode(val1, nodelist_true, nodelist_false, negate) 
 
 
class do_judgeStudentNode(template.Node): 
    child_nodelists = ('nodelist_true', 'nodelist_false') 
 
    def __init__(self, var1, nodelist_true, nodelist_false, negate): 
        self.var1 = var1
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false 
        self.negate = negate 
 
    def __repr__(self): 
        return "<IfEqualNode>" 
 
    def render(self, context): 
        val1 = self.var1.resolve(context, True)
        this_University_info = University_info.objects.get(id=val1.university_info_id)
        if this_University_info.school == 'notStudent' and this_University_info.college== 'notStudent' and this_University_info.major == 'notStudent':
            judge = False
        else:
            judge = True
        if (self.negate and not judge) or (not self.negate and judge): 
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

class showNewsLikeManNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        values = self.sequence.resolve(context, True) 
        user_list = values.split(';')[:-1]
        users = MyUser.objects.filter(id__in=user_list)
        s = ''
        for user in users:
            s += u'%s、' % user.nic_name
        return s[:-1]
        
def showNewsLikeMan(parser, token):
    try:
        tag_name, text_name= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(text_name)    
    return showNewsLikeManNode(sequence)  

class showBewatchedNumNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        values = self.sequence.resolve(context, True) 
        this_user_info = User_info.objects.get(user=values)
        s = ''
        if this_user_info.beWatched:
            n = this_user_info.beWatched.split(';')
            s += '%s人关注ta&nbsp;&nbsp;' % (len(n)-1)
        return s
        
def showBewatchedNum(parser, token):
    try:
        tag_name, text_name= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(text_name)    
    return showBewatchedNumNode(sequence)     
    
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
        elif str(self.sequence) == 'partNews':
            s = ''
            for part in NewsPart.objects.filter(secret=False):
                for small in ['hot','controversial','gilded']:
                    s += 'Allow: /news/%s/%s/\r\n' % (part.part, small)
            return s
        elif str(self.sequence) == 'news':
            s ='' 
            for news in News.objects.filter(secret=False):
                for s1 in ['hot','controversial','gilded']:
                    s += 'Allow: /news/%s/%s/showNews/%s/\r\n' % (news.newspart.part,s1,news.id)
                    if not news.secret:
                        s += 'Allow: /news/All/%s/showNews/%s/\r\n' % (s1,news.id)
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
                s_temp1 = '\r\n   <url>\r\n\r\n      <loc>http://www.funqiu.com/eot/showcredit/%s/</loc>\r\n' % credit.id
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
                s_temp1 = '\r\n   <url>\r\n\r\n      <loc>http://www.funqiu.com/eot/showeot/%s/</loc>\r\n' % eot.id
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
                s_temp1 = '\r\n   <url>\r\n\r\n      <loc>http://www.funqiu.com/eot/showcomment/%s/</loc>\r\n' % eotdata.id
                s_temp2 = '\r\n      <lastmod>%s</lastmod>\r\n' % lastmod
                s_temp3 = '\r\n      <changefreq>weekly</changefreq>\r\n\r\n   </url>\r\n'
                s += s_temp1 + s_temp2 + s_temp3
            return s
        elif str(self.sequence) == 'getCreditFile':
            s = ''
            school_time = '2014-02-24'
            for (k,v) in  code_school.items(): 
                s_temp1 = '\r\n   <url>\r\n\r\n      <loc>http://www.funqiu.com/business/guide/getCreditFile/%s/</loc>\r\n' % k
                s_temp2 = '\r\n      <lastmod>%s</lastmod>\r\n' % school_time
                s_temp3 = '\r\n      <changefreq>yearly</changefreq>\r\n\r\n   </url>\r\n'
                s += s_temp1 + s_temp2 + s_temp3
            return s
        elif str(self.sequence) == 'partNews':
            s = ''
            now = datetime.now()
            if now.month < 10:
                month = '0%s' % now.month
            else:
                month = now.month
            if now.day < 10:
                day = '0%s' % now.day
            else:
                day = now.day
            today = '%s-%s-%s' % (now.year,month,day)
             
            for part in NewsPart.objects.filter(secret=False):
                for small in ['hot','controversial','gilded']:
                    s_temp1 = '\r\n   <url>\r\n\r\n      <loc>http://www.funqiu.com/news/%s/%s/</loc>\r\n' % (part.part, small)
                    s_temp2 = '\r\n      <lastmod>%s</lastmod>\r\n' % today
                    s_temp3 = '\r\n      <changefreq>always</changefreq>\r\n\r\n   </url>\r\n'
                    s += s_temp1 + s_temp2 + s_temp3
            return s
        elif str(self.sequence) == 'news':
            s = ''
            now = datetime.now()
            if now.month < 10:
                month = '0%s' % now.month
            else:
                month = now.month
            if now.day < 10:
                day = '0%s' % now.day
            else:
                day = now.day
            today = '%s-%s-%s' % (now.year,month,day)
            for news in News.objects.filter(secret=False):
                for s1 in ['hot','controversial','gilded']:
                    url = 'http://www.funqiu.com/news/%s/%s/showNews/%s/' % (news.newspart.part,s1,news.id)
                    s_temp1 = '\r\n   <url>\r\n\r\n      <loc>%s</loc>\r\n' % url
                    s_temp2 = '\r\n      <lastmod>%s</lastmod>\r\n' % today
                    s_temp3 = '\r\n      <changefreq>always</changefreq>\r\n\r\n   </url>\r\n'
                    s += s_temp1 + s_temp2 + s_temp3              
                    if not news.secret:
                        url = 'http://www.funqiu.com/news/All/%s/showNews/%s/' % (s1,news.id)
                        s_temp1 = '\r\n   <url>\r\n\r\n      <loc>%s</loc>\r\n' % url
                        s_temp2 = '\r\n      <lastmod>%s</lastmod>\r\n' % today
                        s_temp3 = '\r\n      <changefreq>always</changefreq>\r\n\r\n   </url>\r\n'
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

class showDayNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        values = self.sequence.resolve(context, True)

        nowDay = datetime.now(pytz.utc).day
        thatDay = values.day
        if nowDay == thatDay:
            return '今天'
        elif (nowDay-thatDay) == 1:
            return '昨天'
        elif (nowDay-thatDay) == 2:
            return '前天'
        else:
            return '%s-%s-%s' % (values.year,values.month,values.day)
            
def showDay(parser, token):
    try:
        tag_name, text_name= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(text_name)    
    return showDayNode(sequence)
  
class showTimeHMNode(template.Node):
    def __init__(self,sequence):
        self.sequence = sequence

    def render(self, context):
        values = self.sequence.resolve(context, True)
        hour = values.hour+8
        minute = values.minute
        if hour < 10:
            hour = '0%s' % hour
        if minute < 10:
            minute = '0%s' % minute
        return '%s:%s' % (hour,minute)
            
def showTimeHM(parser, token):
    try:
        tag_name, text_name= token.split_contents() 
    except:
        raise template.TemplateSyntaxError
        
    sequence = parser.compile_filter(text_name)    
    return showTimeHMNode(sequence)
  
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
        try:
            if info.upVoted_news and str(news.id) in info.upVoted_news:
                vote = 'VotedNum'
            if info.downVoted_news and str(news.id) in info.downVoted_news:
                vote = 'VotedNum'
        except:
            pass
            
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
register.tag('showDay', showDay)
register.tag('newsScoreClass', newsScoreClass)
register.tag('showTimeHM', showTimeHM)
register.tag('showNewsLikeMan', showNewsLikeMan)
register.tag('showBewatchedNum', showBewatchedNum)
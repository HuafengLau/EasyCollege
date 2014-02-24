#coding:utf-8

from django import template
from University.models import University_info
from EOT.models import Eot, Eot_data, Eot_data
from Business.models import Credit
from Business.views import code_school

import re

register = template.Library()

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
            num = Credit.objects.all().count()
            s = ''
            for i in xrange(1, num):
                s += 'Allow: /eot/showcredit/%s/\r\n' % i
            return s
        elif str(self.sequence) == 'eot':
            num = Eot.objects.all().count()
            s = ''
            for i in xrange(1, num):
                s += 'Allow: /eot/showeot/%s/\r\n' % i
            return s
        elif str(self.sequence) == 'eotcomment':
            num = Eot_data.objects.all().count()
            s = ''
            for i in xrange(1, num):
                s += 'Allow: /eot/showcomment/%s/\r\n' % i
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
    
register.tag('ShowCourse', ShowCourse)
register.tag('ShowSchool', ShowSchool)
register.tag('Robot', Robot)
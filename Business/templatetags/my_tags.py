#coding:utf-8

from django import template
from University.models import University_info
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
        print 'values:%s' % values
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
    
register.tag('ShowCourse', ShowCourse)
register.tag('ShowSchool', ShowSchool)
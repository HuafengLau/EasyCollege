#coding: utf-8

from django import forms
from News.models import News, NewsPart, NewsPartRule
#from django.utils.translation import ugettext_lazy as _
from rte.kindeditor.widgets import KindEditor

line = '-------请选择---------'

class LinkNewsForm3(forms.ModelForm):
    def __init__(self, *args, **kwargs):   
        self.base_fields['newspart'].queryset = NewsPart.objects.filter(can_link=True).order_by('part')
        super(LinkNewsForm3, self).__init__(*args, **kwargs)  
        
    type = forms.CharField(
        label=u'类型',
        required=True,
        max_length=5,
        widget=forms.TextInput(attrs={'type':'hidden','value':'link','required':"required"}),
        error_messages={
            'required': u'类型是必填项！',
            'max_length': u'类型太长了！'
        }
    )
    
    title = forms.CharField(
        required=True,
        label=u'标题',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':u"尝试想一个有创意的标题吧！",'required':"required"}),
        error_messages={
            'required': u'标题是必填项！',
            'max_length': u'标题太长啦！'
        }
    )
    
    link = forms.URLField(
        required=True,
        label=u'链接',
        max_length=200,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':"e.g. http://www.collegeyi.com",'required':"required"}),
        error_messages={
            'max_length': u'链接太长啦！'
        }
    )
    
    class Meta:
        model = News
        exclude = ('ups','downs','time','gold','score','controversy','hot','user','text','pic','comment_num','mp3')  
 
class LinkNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  
        super(LinkNewsForm, self).__init__(*args, **kwargs)  
        
        self.fields['newspart'].choices = [('', line)] + [
            (part.id, '%s / %s' % (part.part,part.realPart)) for part in NewsPart.objects.filter(can_link=True).exclude(part='All').order_by('part')] 
        self.fields['newspart'].widget.attrs={'class':'form-control pull-left','required':"required"}
    
    type = forms.CharField(
        label=u'类型',
        required=True,
        max_length=5,
        widget=forms.TextInput(attrs={'type':'hidden','value':'link','required':"required"}),
        error_messages={
            'required': u'类型是必填项！',
            'max_length': u'类型太长了！'
        }
    )
     
    #newspart = forms.ChoiceField(
        #label=u'社群',
        #required=True,
        #choices=(),
        #widget=forms.Select(attrs={'class':'form-control pull-left','required':"required"}),
        #error_messages={
        #    'required': u'社群是必填项！',
        #}
    #)
    
    title = forms.CharField(
        required=True,
        label=u'标题',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':u"尝试想一个有创意的标题吧！",'required':"required"}),
        error_messages={
            'required': u'标题是必填项！',
            'max_length': u'标题太长啦！'
        }
    )
    
    link = forms.URLField(
        required=True,
        label=u'链接',
        max_length=200,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':"e.g. http://www.collegeyi.com",'required':"required"}),
        error_messages={
            'max_length': u'链接太长啦！'
        }
    )
    
    class Meta:
        model = News
        exclude = ('ups','downs','time','gold','score','controversy','hot','user','text','pic','comment_num','mp3') 

class TextNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  
        super(TextNewsForm, self).__init__(*args, **kwargs)  

        self.fields['newspart'].choices = [('', line)] + [
            (part.id, '%s / %s' % (part.part,part.realPart)) for part in NewsPart.objects.filter(can_text=True).exclude(part='All').order_by('part')] 
            
        self.fields['newspart'].widget.attrs={'class':'form-control pull-left','required':"required"}
    
    type = forms.CharField(
        label=u'类型',
        required=True,
        max_length=5,
        widget=forms.TextInput(attrs={'type':'hidden','value':'text','required':"required"}),
        error_messages={
            'required': u'类型是必填项！',
            'max_length': u'类型太长了！'
        }
    )
    
    title = forms.CharField(
        required=True,
        label=u'标题',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':u"尝试想一个有创意的标题吧！",'required':"required"}),
        error_messages={
            'required': u'标题是必填项！',
            'max_length': u'标题太长啦！'
        }
    )
    
 
    text = forms.CharField(
        label=u'文章（可选）',
        widget=KindEditor(attrs={'rows':15, 'cols':130}),
    )
    
    class Meta:
        model = News
        exclude = ('ups','downs','time','gold','score','controversy','hot','user','link','pic','comment_num','mp3')

class PicNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  
        super(PicNewsForm, self).__init__(*args, **kwargs)  
        self.fields['newspart'].choices = [('', line)] + [
            (part.id, '%s / %s' % (part.part,part.realPart)) for part in NewsPart.objects.filter(can_pic=True).exclude(part='All').order_by('part')] 
        self.fields['newspart'].widget.attrs={'class':'form-control pull-left','required':"required"}
    
    type = forms.CharField(
        label=u'类型',
        required=True,
        max_length=5,
        widget=forms.TextInput(attrs={'type':'hidden','value':'pic','required':"required"}),
        error_messages={
            'required': u'类型是必填项！',
            'max_length': u'类型太长了！'
        }
    )
    
    title = forms.CharField(
        required=True,
        label=u'标题',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':u"尝试想一个有创意的标题吧！",'required':"required"}),
        error_messages={
            'required': u'标题是必填项！',
            'max_length': u'标题太长啦！'
        }
    )
    
    pic = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class':'form-control','required':"required"}),
        label=u'图片',
        error_messages={
            'required': u'你没有上传图片！',
        }
    )
    
    class Meta:
        model = News
        exclude = ('ups','downs','time','gold','score','controversy','hot','user','link','text','comment_num','mp3')  
        
class mp3NewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):  
        super(mp3NewsForm, self).__init__(*args, **kwargs)  
        self.fields['newspart'].choices = [('', line)] + [
            (part.id, '%s / %s' % (part.part,part.realPart)) for part in NewsPart.objects.filter(can_mp3=True).exclude(part='All') .order_by('part')] 
        self.fields['newspart'].widget.attrs={'class':'form-control pull-left','required':"required"}
    
    type = forms.CharField(
        label=u'类型',
        required=True,
        max_length=5,
        widget=forms.TextInput(attrs={'type':'hidden','value':'mp3','required':"required"}),
        error_messages={
            'required': u'类型是必填项！',
            'max_length': u'类型太长了！'
        }
    )
    
    title = forms.CharField(
        required=True,
        label=u'标题',
        max_length=100,
        widget=forms.TextInput(attrs={'class':'form-control','placeholder':u"尝试想一个有创意的标题吧！",'required':"required"}),
        error_messages={
            'required': u'标题是必填项！',
            'max_length': u'标题太长啦！'
        }
    )
    
    mp3 = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={'class':'form-control','required':"required"}),
        label=u'MP3文件',
        error_messages={
            'required': u'你没有上传MP3！',
        }
    )
    
    class Meta:
        model = News
        exclude = ('ups','downs','time','gold','score','controversy','hot','user','link','text','comment_num','pic') 
        
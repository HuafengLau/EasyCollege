#coding: utf-8

from django import forms
from Index.models import Avatar,Folder

class AvatarForm(forms.ModelForm):
    photo = forms.ImageField(label=u'更改头像',required=True)
    
    class Meta:
        model = Avatar
        exclude = ('user',)
        
class FolderForm(forms.ModelForm):
    name = forms.CharField(
        label=u'收藏夹名',
        required = True,
        max_length=20,
        widget=forms.TextInput(attrs={'required':"required",'class':'form-control width_20','autofocus':'autofocus'}),
        error_messages={
            'required': u'收藏夹名为必填项',
            'max_length': u'收藏夹名字太长啦'
        }
    )
    
    description = forms.CharField(
        label=u'描述',
        required = True,
        max_length=50,
        widget=forms.TextInput(attrs={'required':"required",'class':'form-control'}),
        error_messages={
            'required': u'为收藏夹添加描述有助于区分收藏夹',
            'max_length': u'收藏夹描述太长啦'
        }
    )
    class Meta:
        model = Folder
        exclude = ('owner',)
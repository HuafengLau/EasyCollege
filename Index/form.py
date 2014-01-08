#coding: utf-8

from django import forms
from Index.models import Avatar

class AvatarForm(forms.ModelForm):
    photo = forms.ImageField(label=u'更改头像',required=True)
    
    class Meta:
        model = Avatar
        exclude = ('user',)
#coding: utf-8

from django import forms
from EOT.models import Eot_data, Eot_img

class Eot_dataForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label=u'资料主题',
        max_length=10,
        help_text=u'主题中请包涵平时作业、期末、期中、课件、试题等关键字，10字以内 ',
        error_messages={
            'required': u'你还没有为资料添加主题！',
            'max_length': u'主题不宜超过10个字'
        }
    )
    description = forms.CharField(
        required=True,
        label=u'描述资料',
        max_length=80,
        help_text=u'简要描述文件内容或注意事项，50字以内 ',
        widget=forms.Textarea(attrs={'cols':'50','rows':'3'}),
        error_messages={
            'required': u'你还没有为资料添加说明！',
            'max_length': u'描述不宜超过30字！'
        }
    )
    price_num = forms.IntegerField(
        required=True,
        label=u'资料定价',
        max_value=40,
        min_value=0,
        help_text=u'填整数。对于单个文件，不推荐价格超过10易币；对于内涵多个文件如课件包，推荐价格超过35易币',
        widget=forms.TextInput(attrs={'size':'3'}),
        error_messages={
            'required': u'你还没有为资料定价，如果你希望资料免费，你可以填0',
            'max_value': u'目前大学易不推荐如此高的定价！',
            'min_value': u'如果你希望资料免费，你可以填0'
        }
    )
    file = forms.FileField(
        required=True,
        label=u'文件',
        help_text=u'推荐上传压缩包，特别是课件集。文件大小不应超过30M',
        error_messages={
            'required': u'你还没有上传资料！',
        }
    )
    
    class Meta:
        model = Eot_data
        exclude = ('value_like_num','value_hate_num','warning_num','download_num','upload_time','owner','eot','profit')
        
class Eot_imgForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label=u'图片标题',
        max_length=10,
        help_text=u'主题中请务必表明时间，如：2011级教材。10字以内 ',
        error_messages={
            'required': u'你还没有为图片添加主题！',
            'max_length': u'主题不宜超过10个字'
        }
    )
    description = forms.CharField(
        required=True,
        label=u'描述图片',
        max_length=40,
        help_text=u'简要描述图片，40字以内 ',
        widget=forms.Textarea(attrs={'cols':'50','rows':'3'}),
        error_messages={
            'required': u'你还没有为图片添加说明！',
            'max_length': u'描述不宜超过40字！'
        }
    )

    img = forms.ImageField(
        required=True,
        label=u'图片',
        help_text=u'请确保图片与课程相关，文件名称不要使用中文',
        error_messages={
            'required': u'你还没有上传图片！',
        }
    )
    
    class Meta:
        model = Eot_img
        exclude = ('like_num','upload_time','owner','eot','if_safe')         
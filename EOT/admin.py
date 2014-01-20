#coding:utf-8

from django.contrib import admin
from EOT.models import *


class TeacherAdmin(admin.ModelAdmin):
    """docstring for TeacherAdmin"""
    list_display = ('university','name','value_num','avg_score')
    list_filter = ('university','name')
    ordering = ('university','name')
        
class EotAdmin(admin.ModelAdmin):
    """docstring for EotAdmin"""
    list_display = ('university','college','course', 'teacher', 'value_num',
        'course_avg_score','teacher_avg_score','history_avg_score','like_num','middle_num','dead_num',
        'hate_num','recommend_num')
    list_filter = ('university',)
    ordering = ('university', )
    
class First_3Admin(admin.ModelAdmin):
    """docstring for First_3Admin"""
    list_display = ('eot','user', 'lucky')
    list_filter = ('lucky',)
    ording = ('eot','lucky')

class Eot_commentAdmin(admin.ModelAdmin):
    """docstring for Eot_commentAdmin"""
    list_display = ('eot','user', 'agree_num','disagree_num','time')
    list_filter = ('eot',)
    ording = ('eot',)
    
class Eotdata_commentAdmin(admin.ModelAdmin):
    """docstring for Eot_commentAdmin"""
    list_display = ('eot_data','user','time')
    list_filter = ('eot_data',)
    ording = ('eot_data',)
 
class Eot_namingAdmin(admin.ModelAdmin):
     """docstring for Eot_namingAdmin"""
     list_display = ('never_num', 'sometimes_num', 'often_num')

class Eot_naming_wayAdmin(admin.ModelAdmin):
    """docstring for Eot_naming_wayAdmin"""
    list_display = ('no_num', 'sign_num', 'answer_num','hybrid_num')
    
class Eot_atmosphereAdmin(admin.ModelAdmin):
    """docstring for Eot_atmosphereAdmin"""
    list_display = ('dead_num', 'normal_num', 'active_num')
    
class Eot_teach_wayAdmin(admin.ModelAdmin):
    """docstring for Eot_teach_wayAdmin"""
    list_display = ('PPT_num', 'book_num', 'teacher_num','hybrid_num') 
   
class Eot_popularityAdmin(admin.ModelAdmin):
    """docstring for Eot_popularityAdmin"""
    list_display = ('most_num', 'more_num', 'less_num','nobody_num')

class Eot_mid_test_wayAdmin(admin.ModelAdmin):
    """docstring for Eot_mid_test_wayAdmin"""
    list_display = ('no_num', 'paper_num', 'pravite_num','inspect_num')   
   
class Eot_final_test_wayAdmin(admin.ModelAdmin):
    """docstring for Eot_final_test_wayAdmin"""
    list_display = ('paper_num', 'pravite_num', 'inspect_num')

class Eot_revealAdmin(admin.ModelAdmin):
    """docstring for Eot_revealAdmin"""
    list_display = ('draw_importence_num', 'give_paper_num', 'others_num','nothing_num') 

class Eot_usual_workAdmin(admin.ModelAdmin):
    """docstring for Eot_usual_workAdmin"""
    list_display = ('less_num', 'some_num', 'more_num') 

class Eot_mid_testAdmin(admin.ModelAdmin):
    """docstring for Eot_mid_testAdmin"""
    list_display = ('yes_num', 'no_num')     
 
class Eot_dataAdmin(admin.ModelAdmin): 
    """docstring for Eot_dataAdmin"""
    list_display = ('title','owner', 'eot','price_num','warning_num','file','upload_time')
    list_filter = ('eot','price_num','warning_num','upload_time')
    ording = ('eot','owner','value_like_num') 
    
class Eot_imgAdmin(admin.ModelAdmin): 
    """docstring for Eot_imgAdmin"""
    list_display = ('title','owner', 'eot','like_num','img','upload_time','if_safe')
    list_filter = ('eot','like_num','upload_time')
    ording = ('eot','owner','like_num') 
 
admin.site.register(Eot_img, Eot_imgAdmin)
admin.site.register(Eot_data, Eot_dataAdmin) 
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Eot, EotAdmin)
admin.site.register(First_3, First_3Admin)
admin.site.register(Eot_comment, Eot_commentAdmin)
admin.site.register(Eotdata_comment, Eotdata_commentAdmin)
admin.site.register(Eot_naming, Eot_namingAdmin)
admin.site.register(Eot_naming_way, Eot_naming_wayAdmin)
admin.site.register(Eot_atmosphere, Eot_atmosphereAdmin)
admin.site.register(Eot_teach_way, Eot_teach_wayAdmin)
admin.site.register(Eot_popularity, Eot_popularityAdmin)
admin.site.register(Eot_mid_test_way, Eot_mid_test_wayAdmin)
admin.site.register(Eot_final_test_way, Eot_final_test_wayAdmin)
admin.site.register(Eot_reveal, Eot_revealAdmin)
admin.site.register(Eot_usual_work, Eot_usual_workAdmin)
admin.site.register(Eot_mid_test, Eot_mid_testAdmin)
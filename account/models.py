#coding:utf-8

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone



class MyUserManager(BaseUserManager):
    def create_user(self, stu_ID, stu_pwd, name, nic_name, email, money,
        university_info_id,first_value, avatar,**extra_fields):
        
        now = timezone.now()
        
        if not email:
            raise ValueError('The given email must be set')
            
        email = MyUserManager.normalize_email(email)
        
        user = self.model(stu_ID=stu_ID, stu_pwd=stu_pwd, name=name, nic_name=nic_name,
            email=email, money=money,university_info_id= university_info_id,
            first_value=first_value, last_login=now, avatar=avatar,**extra_fields)
                          
        user.set_password(stu_pwd)
        
        user.save(using=self._db)
        
        return user
        
    
    def create_superuser(self, stu_ID, stu_pwd, name, nic_name, email, money,
        university_info_id,first_value,avatar,**extra_fields):
        
        now = timezone.now()
        
        user = self.create_user(stu_ID, stu_pwd, name, nic_name, email, money,
            university_info_id,first_value,avatar, **extra_fields)
            

        user.is_acitve=True
        user.is_admin=True

        user.save(using=self._db)
        return user
        
class MyUser(AbstractBaseUser, PermissionsMixin):
    stu_ID = models.CharField(max_length=20,)
    stu_pwd = models.CharField(max_length=20)
    name = models.CharField(max_length=25,null=True, blank=True)
    nic_name = models.CharField(max_length=20)
    email = models.EmailField(verbose_name='email', unique=True)
    money = models.IntegerField(verbose_name=u'money')
    university_info_id = models.CharField(max_length=30,verbose_name='school_id')
    first_value = models.IntegerField(verbose_name=u'honour')
    avatar = models.CharField(max_length=200,null=True,blank=True)
    
    
    
    is_admin = models.BooleanField('staff status', default=False,
        help_text='flag for log into admin site.')
        
    is_active = models.BooleanField('active', default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['stu_ID', 'stu_pwd', 'name', 'nic_name', 'money',
        'university_info_id','first_value','avatar']
    objects = MyUserManager()
    
    def get_full_name(self):
        return self.stu_ID
        
    def get_short_name(self):
        return self.stu_ID
        
    def __unicode__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
        
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app 'app_label'?"
        # Simplest possible answer: Yes, always
        return True
        
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


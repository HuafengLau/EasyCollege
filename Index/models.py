from django.db import models
from account.models import MyUser

# Create your models here.
class Avatar(models.Model):
    photo = models.ImageField(upload_to='avatar/',blank=True,null=True)
    user = models.ForeignKey(MyUser,related_name="profile",blank=True,null=True)
    
    def __unicode__(self):
        return '%s' % (self.user)
        

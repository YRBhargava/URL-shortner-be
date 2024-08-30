from typing import Any
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

#--------THIS IS USER MODEL-------------------
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    name=models.CharField(max_length=20,null=False, blank=False )
    email=models.EmailField(max_length=20, null=False, blank=False)
    phone = models.CharField(
        max_length=10, 
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be exactly 10 digits.', code='invalid_phone')],
        null=False, 
        blank=False
    )
    password=models.CharField(max_length=100 ,null=False, blank=False)
    
    def __str__(self):
        return (self.name, self.email, self.phone)
    
    
#---------THIS IS URL MODEL-------------------------
class Url(models.Model):
    userId = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='urls')
    originalUrl=models.CharField(max_length=100, blank=False, null=False)
    shortUrl=models.CharField(max_length=50, null=False, blank=False,unique=True)
    creationDate = models.DateTimeField(null=False,blank=False,default=timezone.now())    
    def __str__(self):
        return (self.userId,self.originalUrl,self.shortUrl)
    
    
    
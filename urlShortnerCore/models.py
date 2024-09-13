from typing import Any
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None):
        if not email:
            raise ValueError('The Email field is required')
        if not name:
            raise ValueError('The Name field is required')

        user = self.model(
            email=self.normalize_email(email),
            name=name,
            phone=phone,
        )
        user.password = make_password(password)
        user.save(using=self._db)
        return user

#--------THIS IS USER MODEL-------------------
class User(AbstractBaseUser):
    userId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=50, null=False, blank=False, unique=True)
    phone = models.CharField(
        max_length=10, 
        validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be exactly 10 digits.', code='invalid_phone')],
        null=False, 
        blank=False
    )
    password = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']
    objects = UserManager()

    def __str__(self):
        return f'{self.name} ({self.email})'



#---------THIS IS URL MODEL-------------------------
class Url(models.Model):
    userId = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='urls')
    originalUrl=models.CharField(max_length=100, blank=False, null=False)
    shortUrl=models.CharField(max_length=50, null=False, blank=False,unique=True)
    creationDate = models.DateTimeField(null=False,blank=False,default=timezone.now())    
    def __str__(self):
        return f'{self.userId},{self.originalUrl},{self.shortUrl}'
    
    
    
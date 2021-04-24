from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone



class MyAccountManager(BaseUserManager):
    def create_user(self, email,password=None,**kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
			**kwargs
		)
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password,**kwargs):
        user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			**kwargs
		)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
 


class Account(AbstractBaseUser, PermissionsMixin):
    email=models.EmailField(verbose_name="email", max_length=160, unique=True)
    registration_number=models.CharField(max_length=9, unique=True)
    first_name= models.CharField(max_length=100)
    last_name= models.CharField(max_length=100)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login=models.DateTimeField(default=timezone.now)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False) 
    is_superuser=models.BooleanField(default=True)
    
 
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','registration_number']
    
    objects = MyAccountManager()
    
    def __str__(self):
        return self.email
    
	# For checking permissions. to keep it simple all admin have ALL permissons
    # def has_perm(self, perm, obj=None):
    #     return self.is_staff
    
	# # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    # def has_module_perms(self, app_label):
    #     return True
    
     
from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
# from django.contrib.postgres.fields import ArrayField


# Create your models here.


class CustomUserManager(UserManager):
  def _create_user(self, email, password, **extra_fields):
    if not email:
      raise ValueError('You have not provided a valid email')
    
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    
    return user

  def create_user(self, email=None, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email=None, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    extra_fields.setdefault('is_active', True)
    return self._create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
  email = models.EmailField(unique=True)
  firstName = models.CharField(max_length=255, blank=True, default='')
  lastName = models.CharField(max_length=255, blank=True,  default='')
  friends = models.JSONField(default=dict, blank=True)
  picturePath = models.ImageField(upload_to='media/', default='', blank=True)
  location = models.CharField(max_length=255)
  occupation = models.CharField(max_length=255)
  viewedProfile = models.IntegerField(default=0)
  impressions = models.IntegerField(default=0)

  #require to have permissionsMixin
  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=True)

  date_joined = models.DateTimeField(default=timezone.now)
  last_login = models.DateTimeField(blank=True, null=True)
  
  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  EMAIL_FIELD= 'email'
  REQUIRED_FIELDS = []

  class Meta:
    verbose_name = 'User'
    verbose_name_plural = 'Users'

  def get_full_name(self):
    return self.firstName + ' ' + self.lastName
  
  def get_short_name(self):
    return self.email.split('@')[0]

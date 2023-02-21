from django.db import models
from django.contrib.postgres.fields import ArrayField
from authuser.models import User

# Create your models here.

class Post(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userId')
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    image = models.ImageField(upload_to='media/', default='')
    userPicturePath = models.CharField(max_length=255, default='')
    likes = models.JSONField(default=dict, blank=True)
    comments = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return str(self.id)

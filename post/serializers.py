from rest_framework import serializers
from .models import Post
from authuser.models import User
from authuser.serializers import MyUserSerializer


class PostSeralizer(serializers.ModelSerializer):
  # user = MyUserSerializer()
  
  class Meta:
    model = Post
    fields = (
      'userId',
      'firstname',
      'lastName',
      'location',
      'description',
      'image',
      'likes',
      'comments',
    )

    def create(self, validated__date):
      post_data = validated__date
      post = Post.objects.create(**post_data)
      return post
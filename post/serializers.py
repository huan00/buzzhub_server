from rest_framework import serializers
from .models import Post
from authuser.models import User
from authuser.serializers import MyUserSerializer


class PostSerializer(serializers.ModelSerializer):

  class Meta:
    model = Post
    fields = (
      'id',
      'userId',
      'firstName',
      'lastName',
      'location',
      'description',
      'image',
      'likes',
      'video',
      'comments',
      'userPicturePath'
    )

    def create(self, validated__data):
      post_data = validated__data
      post = Post.objects.create(**post_data)
      return post
  
  class PostVideoSerializer(serializers.ModelSerializer):

    class Meta:
      model = Post
      fields = (
      'id',
      'userId',
      'firstName',
      'lastName',
      'location',
      'description',
      'video',
      'likes',
      'comments',
      'userPicturePath'
    )

    def create(self, validated__date):
      post_data = validated__date
      post = Post.objects.create(**post_data)
      return post

# class GetPostSerializer(serializers.ModelSerializer):

#   class Meta:

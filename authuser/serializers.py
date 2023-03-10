from rest_framework import serializers
from .models import User

class MyUserCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      'firstName',
      'lastName',
      'email',
      'password',
      'picturePath',
      'location',
      'occupation',
    )
  
  def create(self, validated_data):
    password = validated_data.pop('password')
    user = User(**validated_data)
    user.set_password(password)
    user.save()
    return user

class MyUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      'id',
      'firstName',
      'lastName',
      'friends',
      'email',
      'picturePath',
      'location',
      'occupation',
      'viewedProfile',
      'impressions',
    )
  
class MyUserPostSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      'id',
      'firstName',
      'lastName',
      'location',
      'picturePath'
    )

class MyUserFriendSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = (
      'friends',
    )

  def create(self, data):
  
    list = data.pop('friends')
    friendList = []
    for friend in list:
        data = User.objects.get(id=int(friend))
        friendList.append(MyUserSerializer(data).data)
    
    return friendList
  
class MyFriendListSerializer(serializers.ModelSerializer):
  class Meta: 
    model = User
    fields = (
      'firstName',
      'lastName',
      'location',
      'picturePath',
      'id',
      'occupation'
    )

# class MyPostSerializer(serializers.ModelSerializer):
#   # userId = MyUserSerializer()
#   class Meta: 
#     model = Post
#     fields = (
#       'userId',
#       'firstName',
#       'lastName',
#       'location',
#       'description',
#       'image',
#       'likes',
#       'comments',
#     )
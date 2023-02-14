from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Post
from .serializers import PostSerializer
from authuser.models import User
from authuser.serializers import MyUserSerializer, MyUserPostSerializer

# Create your views here.

@api_view(['POST'])
def createPost(request):
    print(request.data)
    userId, description, image = request.data.values()
    userSerializer = MyUserPostSerializer(User.objects.get(id=userId)).data
    userImage = userSerializer['image']
    firstName = userSerializer['firstName']
    lastName = userSerializer['lastName']
    location = userSerializer['location']
    print(userImage)

    postData = {'userId': userId, 'firstName': firstName, 'lastName': lastName, 'location': location, 'description': description}

    postSerializer = PostSerializer(data=postData)
    if postSerializer.is_valid():
        postSerializer.save()
    else:
        print('not valid')



    return Response(postSerializer.data)
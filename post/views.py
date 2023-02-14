from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Post
from .serializers import PostSerializer
from authuser.models import User
from authuser.serializers import MyUserSerializer, MyUserPostSerializer

# Create your views here.

@api_view(['POST'])
def createPost(request):
    userId = request.data['userId']
    userSerializer = MyUserPostSerializer(User.objects.get(id=userId)).data
    postData = {
        **request.data
    }
    print(postData)
    postSerializer = PostSerializer(data=postData)
    if postSerializer.is_valid():
        postSerializer.save()
        return Response(postSerializer.data)
    else:
        return Response({"error": "something went wrong"})


@api_view(['GET'])
def getPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


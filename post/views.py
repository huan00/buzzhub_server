from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, authentication

from .models import Post
from .serializers import PostSerializer
from authuser.models import User
from authuser.serializers import MyUserSerializer, MyUserPostSerializer

# Create your views here.

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def createPost(request, format=None):
    userId = request.data['userId']
    description = request.data['description']
    image = request.data['image']

    userSerializer = MyUserPostSerializer(User.objects.get(id=userId)).data

    
    postData = {
        'userId': userId, 
        'firstName': userSerializer['firstName'], 
        'lastName': userSerializer['lastName'], 
        'location': userSerializer['location'], 
        'image': image, 
        'description': description, 
        'userPicturePath': userSerializer['picturePath']
        }

    postSerializer = PostSerializer(data=postData)
    if postSerializer.is_valid():
        postSerializer.save()
        posts = Post.objects.all().order_by('-id')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "something went wrong"})


@api_view(['GET'])
def getPosts(request):
    posts = Post.objects.all().order_by('-id')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)



@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUserPosts(request, pk):
    
    posts = Post.objects.filter(userId=pk)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['PATCH'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def likePost(request, pk):
    user = User.objects.get(email=request.user)
    userSerializer = MyUserSerializer(user).data
    
    post = Post.objects.get(id=pk)
    postSerializer = PostSerializer(post)

    likes = postSerializer.data['likes']

    if str(userSerializer['id']) in likes:
        likes.pop(str(userSerializer['id']), None)
    else:
        likes[str(userSerializer['id'])] = True

    postSerializer = PostSerializer(post, data={'likes': likes}, partial=True)

    if postSerializer.is_valid():
        postSerializer.save()
        return Response(postSerializer.data, status=status.HTTP_202_ACCEPTED )
    else:
        return Response({'message': 'Something went wrong'}, status=status.HTTP_406_NOT_ACCEPTABLE )

@api_view(['PATCH'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def commentPost(request, pk):
    user = User.objects.get(email=request.user)
    # userSerializer = MyUserSerializer(user)

    post = Post.objects.get(id=pk)
    postSerializer = PostSerializer(post)

    comments = postSerializer.data.pop('comments')
    comments[str(len(comments))] = request.data['comment']
    postSerializer= PostSerializer(post, data={'comments': comments}, partial=True)
    if postSerializer.is_valid():
        postSerializer.save()
        
        return Response(postSerializer.data)
    else:
        return Response({'message': 'something went wrong'})

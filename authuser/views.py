from django.shortcuts import render, get_object_or_404
# from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from .models import User
from post.models import Post
from post.serializers import PostSerializer
from rest_framework import generics
from rest_framework import status, authentication, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout


from .serializers import MyUserSerializer, MyUserFriendSerializer, MyUserCreateSerializer, MyFriendListSerializer
# Create your views here.

@api_view(['POST'])
def registerUser(request):
    exist = User.objects.filter(email = request.data['email']).exists()
    if exist:
        return Response({"error": "User already exist"}, status=status.HTTP_409_CONFLICT)

    serializer = MyUserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create(serializer.data)
        user = User.objects.get(email=user)
        user = MyUserSerializer(user, data={'picturePath': request.FILES['picturePath']}, partial=True)
        if user.is_valid():
            user.save()
            return Response(user.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"error": "Please check submit info"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@csrf_exempt
def loginUser(request, format=None):
    email = request.data['email']
    password = request.data['password']
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request,user)
        token, create = Token.objects.get_or_create(user=request.user)
        data = {
            'token': token.key,
            'user': MyUserSerializer(user).data
        }
        return Response({"data": data}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "invalid login details"}, status=status.HTTP_401_UNAUTHORIZED)

# get user info
@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUser(request, pk):
    viewer = request.user
    user = User.objects.get(id=pk)
    serializer = MyUserSerializer(user)
    if str(viewer) != str(serializer.data['email']):
        viewedProfile = serializer.data.pop('viewedProfile')
        viewedProfile += 1
        updatedSerializer = MyUserSerializer(user, data={'viewedProfile': viewedProfile}, partial=True)
        if updatedSerializer.is_valid():
            updatedSerializer.save()
            return Response(updatedSerializer.data, status=status.HTTP_200_OK)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def getUserFriends(request, pk):
    user = User.objects.get(id=pk)
    serializer = MyUserFriendSerializer(user)
    friendList = serializer.data.pop('friends')
    friends = []
    for friend in friendList:
        temp = User.objects.get(id=friend)
        friendSerializer = MyFriendListSerializer(temp)
        friends.append(friendSerializer.data)

    return Response(friends, status=status.HTTP_200_OK)


# add or remove a friend from user
@api_view(['PATCH'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def addRemoveFriend(request, pk, friendId):
    user = User.objects.get(id=pk)

    serializer = MyUserFriendSerializer(user)

    friends = serializer.data['friends']

    if str(friendId) in friends:
        friends.pop(str(friendId), None)
    else:
        friends[str(friendId)] = True
    
    serializer = MyUserFriendSerializer(user, data={'friends':friends})
    if serializer.is_valid():
        serializer.save()
    else:
        print('not valid')

    userSerializer = MyUserSerializer(user)

    return Response(userSerializer.data)


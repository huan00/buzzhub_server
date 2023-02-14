from django.shortcuts import render, get_object_or_404
# from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from .models import User
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


from .serializers import MyUserSerializer, MyUserFriendSerializer, MyUserCreateSerializer
# Create your views here.

@api_view(['POST'])
def registerUser(request):
    serializer = MyUserCreateSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create(serializer.data)
        user = MyUserSerializer(user)
        return JsonResponse(user.data)
    else:
        return JsonResponse({"message":"something went wrong"})

@api_view(['POST'])
@csrf_exempt
def loginUser(request, format=None):
    email, password = request.data.values()
    user = authenticate(email=email, password=password)
    if user is not None:
        login(request,user)
        print(user.id)
        token, create = Token.objects.get_or_create(user=request.user)
        data = {
            'token': token.key,
            # 'create': create,
            'user': MyUserSerializer(user).data
        }
        return JsonResponse({"data": data})
    else:
        return Response({"error": "invalid login details"})

# get user info
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = MyUserSerializer(user)
    print(serializer.data.id)

    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def getUserFriends(request, pk):
    user = User.objects.get(id=pk)
    serializer = MyUserFriendSerializer(user)
    serializer = serializer.create(serializer.data)
    # friendList = []
    # for friend in serializer.data['friends']:
    #     data = User.objects.get(id=int(friend))
    #     friendList.append(MyUserSerializer(data).data)
    
    return Response(serializer)

# add or remove a friend from user
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def addRemoveFriend(request, pk, friendId):
    user = User.objects.get(id=pk)
    serializer = MyUserFriendSerializer(user)

    friends = serializer.data['friends']
    
    if str(friendId) in friends:
        friends.remove(str(friendId))
    else: 
        friends.append(str(friendId))
    
    serializer = MyUserFriendSerializer(user, data={'friends':friends})
    if serializer.is_valid():
        serializer.save()
    else:
        print('not valid')

    serializer = serializer.create(serializer.data)
        
    return Response(serializer)


# @api_view(['POST'])
# def createPost(request):
#     print(request.data)
#     userId, description, image = request.data.values()
#     userSerializer = MyUserPostSerializer(User.objects.get(id=userId)).data
#     userImage = userSerializer['image']
#     firstName = userSerializer['firstName']
#     lastName = userSerializer['lastName']
#     location = userSerializer['location']
#     print(userImage)

#     postData = {'userId': userId, 'firstName': firstName, 'lastName': lastName, 'location': location, 'description': description}

#     postSerializer = MyPostSerializer(data=postData)
#     if postSerializer.is_valid():
#         postSerializer.save()
#     else:
#         print('not valid')



#     return Response(postSerializer.data)
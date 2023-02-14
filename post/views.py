from django.shortcuts import render
from .models import Post

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

    postSerializer = MyPostSerializer(data=postData)
    if postSerializer.is_valid():
        postSerializer.save()
    else:
        print('not valid')



    return Response(postSerializer.data)
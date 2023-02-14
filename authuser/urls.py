from django.urls import path, include
# from .views import getUser, LoginUser

from . import views

urlpatterns = [
  path('user/<int:pk>/friends', views.getUserFriends),
  path('user/<int:pk>/<int:friendId>', views.addRemoveFriend),
  path('user/<int:pk>', views.getUser ),
  path('user/register', views.registerUser),
  path('user/login', views.loginUser),
  # path('user/viewpost', views.viewPost),
  # path('user/login', LoginUser.as_view())
]
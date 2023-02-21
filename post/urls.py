from django.urls import path, include
from . import views

urlpatterns = [
  path('posts', views.getPosts),
  path('posts/<int:pk>', views.getUserPosts),
  path('posts/likes/<int:pk>', views.likePost),
  path('posts/comment/<int:pk>', views.commentPost),
  path('posts/create', views.createPost),
]
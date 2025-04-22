from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.user_feed, name='user_feed'),  # User feed
    path('feed/group/<str:group_id>/', views.group_feed, name='group_feed'),  # Group feed
    path('create_post/', views.create_post, name='create_post'),  # Create a post (personal)
    path('create_post/<str:group_id>/', views.create_post, name='create_post_group'),  # Create a group post
    path('like_post/<str:post_id>/', views.like_post, name='like_post'),  # Like a post
    path('join_group/<str:group_id>/', views.join_group, name='join_group'),  # Join a group
]

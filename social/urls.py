from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.user_feed, name='user_feed'),  # User's feed (posts)
    path('group/<group_id>/feed/', views.group_feed, name='group_feed'),  # Group feed
    path('post/create/', views.create_post, name='create_post'),  # Create post
    path('post/<post_id>/like/', views.like_post, name='like_post'),  # Like post
    path('group/<group_id>/join/', views.join_group, name='join_group'),  # Join group
]
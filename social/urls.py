from django.urls import path
from . import views

urlpatterns = [
    path('', views.social_hub, name='social_hub'),
    path('add-friend/<str:friend_id>/', views.add_friend, name='add_friend'),
    path('join-group/<str:group_id>/', views.join_group, name='join_group'),
    path('group/<str:group_id>/', views.group_feed, name='group_feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<str:group_id>/create/', views.create_post, name='create_group_post'),
    path('post/<str:post_id>/like/', views.like_post, name='like_post'),
    path('comment/add/', views.add_comment, name='add_comment'),
]
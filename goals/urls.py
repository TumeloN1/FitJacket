from django.urls import path
from . import views

app_name = "goals"

urlpatterns = [
    path('', views.goal_home, name='goal_home'),
    path("create/", views.create_goal, name="create_goal"),
    path("my-goals/", views.view_goals, name="view_goals"),
    path("goal/<int:goal_id>/", views.goal_detail, name="goal_detail"),
    path("edit/<int:goal_id>/", views.update_goal, name="update_goal"),
    path("delete/<int:goal_id>/", views.delete_goal, name="delete_goal"),
]

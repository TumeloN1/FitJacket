from django.urls import path
from . import views

app_name = "goals"

urlpatterns = [
    path('', views.goal_home, name='goal_home'),
    path("create/", views.create_goal, name="create_goal"),
    path("my-goals/", views.view_goals, name="view_goals"),
]

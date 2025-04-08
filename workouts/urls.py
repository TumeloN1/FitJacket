from django.urls import path
from . import views

app_name = "workouts"

urlpatterns = [
    path("plan/", views.view_workout_plan, name="view_plan"),
    path("log/", views.log_workout, name="log_workout"),
    path("recommendations/", views.recommend_workout, name="recommend_workout"),
    path("exercises/", views.exercise_list, name="exercise_list"),
]

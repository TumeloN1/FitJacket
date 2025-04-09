
from django.urls import path
from django.contrib.auth.decorators import login_required
from workouts import views
from workouts.exercise_views import exercises

app_name = "workouts"

urlpatterns = [
    path('plan/', login_required(views.view_workout_plan), name="view_plan"),
    path('log/', login_required(views.log_workout), name="log_workout"),
    path('log/edit/<int:log_id>/', login_required(views.edit_workout_log), name="edit_workout_log"),
    path('log/delete/<int:log_id>/', login_required(views.delete_workout_log), name="delete_workout_log"),
    path('recommend/', login_required(views.recommend_workout), name="recommend_workout"),
    path('exercises/', views.exercise_list, name="exercise_list"),
    path("exercises/browse/", exercises.browse_exercises, name="browse_exercises"),

    path("api/exercises/", exercises.api_exercises_list, name="api_exercises_list"),
    path("api/exercises/bodyPartList/", exercises.api_bodypart_list, name="api_bodypart_list"),
    path("api/exercises/equipmentList/", exercises.api_equipment_list, name="api_equipment_list"),
    path("api/exercises/targetList/", exercises.api_target_list, name="api_target_list"),

    path("api/exercises/bodyPart/<str:bodypart>/", exercises.api_exercises_by_bodypart, name="api_exercises_by_bodypart"),
    path("api/exercises/equipment/<str:equipment>/", exercises.api_exercises_by_equipment, name="api_exercises_by_equipment"),
    path("api/exercises/target/<str:target>/", exercises.api_exercises_by_target, name="api_exercises_by_target"),
    path("api/exercises/name/<str:name>/", exercises.api_exercises_by_name, name="api_exercises_by_name"),
    path("api/exercises/detail/<str:exercise_id>/", exercises.api_exercise_detail, name="api_exercise_detail"),
]

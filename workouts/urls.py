from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from . import exercises_views as api

app_name = "workouts"

urlpatterns = [
    path('plan/', login_required(views.view_workout_plan), name="view_plan"),
    path('log/', login_required(views.view_logs), name="log_home"),
    path('log/create', login_required(views.log_workout), name="log_workout"),
    path('log/edit/<int:log_id>/', login_required(views.edit_workout_log), name="edit_workout_log"),
    path('log/delete/<int:log_id>/', login_required(views.delete_workout_log), name="delete_workout_log"),
    path('recommend/', login_required(views.recommend_workout), name="recommend_workout"),
    path('exercises/', login_required(views.exercise_list), name="exercise_list"),
    path('workout/view/<str:exercise>/', views.view_workout, name='view_workout'),

    # Section browse pages
    path('exercises/bodypart-browse/', login_required(api.bodypart_browse_view), name="bodypart_browse"),
    path('exercises/target-browse/', login_required(api.target_browse_view), name="target_browse"),
    path('exercises/equipment-browse/', login_required(api.equipment_browse_view), name="equipment_browse"),

    # API calls
    path('api/exercises/', login_required(api.api_exercises_list), name="api_exercises_list"),
    path('api/exercises/bodyPart/<str:bodypart>/', login_required(api.api_exercises_by_bodypart), name="api_exercises_by_bodypart"),
    path('api/exercises/equipment/<str:equipment>/', login_required(api.api_exercises_by_equipment), name="api_exercises_by_equipment"),
    path('api/exercises/target/<str:target>/', login_required(api.api_exercises_by_target), name="api_exercises_by_target"),
    path('api/exercises/targets/', login_required(api.api_target_list),name="api_target_list"),
    path('api/exercises/bodyparts/', login_required(api.api_bodypart_list), name="api_bodypart_list"),
    path('api/exercises/equipmentlist/',login_required(api.api_equipment_list),name="api_equipment_list"),

    path('exercises/cache/', login_required(api.cache_dump_html),name='cache_dump_html'),
    path('exercises/detail/<str:exercise_id>/', login_required(api.exercise_detail_view), name="exercise_detail"),
    path('exercises/save/<str:exercise_id>/', login_required(api.save_exercise_view), name="save_exercise"),
    path('exercises/add/', login_required(views.add_exercises_home), name="add_exercises"),
    path('exercises/delete/<int:pk>/', login_required(views.delete_saved_exercise), name="delete_exercise"),
]
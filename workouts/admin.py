# workouts/admin.py
from django.contrib import admin
from .models import WorkoutPlan, WorkoutLog
from accounts.documents import Account

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'goal', 'created_at')
    search_fields = ('user', 'name', 'goal')


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'date', 'sets', 'reps')
    search_fields = ('user', 'exercise')

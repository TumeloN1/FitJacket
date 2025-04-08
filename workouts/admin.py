from django.contrib import admin
from .models import WorkoutPlan, WorkoutLog

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "goal", "created_at")
    search_fields = ("user__username", "name", "goal")
    list_filter = ("created_at",)

@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "exercise", "sets", "reps", "weight", "distance", "duration")
    search_fields = ("user__username", "exercise")
    list_filter = ("date", "exercise")

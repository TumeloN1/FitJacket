from django.contrib import admin
from .models import FitnessGoal

@admin.register(FitnessGoal)
class FitnessGoalAdmin(admin.ModelAdmin):
    list_display = ("user", "goal_type", "target_metric", "target_date", "created_at")
    search_fields = ("user__username", "target_metric")
    list_filter = ("goal_type", "created_at")

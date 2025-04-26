from django.contrib import admin
from .models import Milestones, Badge

@admin.register(Milestones)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "target_category", "target_metric")
    search_fields = ("name", "description")

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "date", "milestone")
    search_fields = ("user", "name", "date", "milestone")

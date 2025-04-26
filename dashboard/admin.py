from django.contrib import admin
from .models import WeightLog, Badge, Milestones

# Register your models here.
@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "weight")
    search_fields = ("user", "date")

@admin.register(Milestones)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "target_category", "target_metric")
    search_fields = ("name", "description")

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "date", "milestone")
    search_fields = ("user", "name", "date", "milestone")

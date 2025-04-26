from django.contrib import admin
from .models import WeightLog

# Register your models here.
@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ("user", "date", "weight")
    search_fields = ("user", "date")

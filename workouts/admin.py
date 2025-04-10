# workouts/admin.py
from django.contrib import admin
from .models import WorkoutPlan, WorkoutLog
from accounts.documents import Account

@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'goal', 'created_at')
    search_fields = ('account_id', 'name', 'goal')

    def username(self, obj):
        acct = Account.objects(id=obj.account_id).first()
        return acct.username if acct else obj.account_id
    username.short_description = 'User'


@admin.register(WorkoutLog)
class WorkoutLogAdmin(admin.ModelAdmin):
    list_display = ('username', 'exercise', 'date', 'sets', 'reps')
    search_fields = ('account_id', 'exercise')

    def username(self, obj):
        acct = Account.objects(id=obj.account_id).first()
        return acct.username if acct else obj.account_id
    username.short_description = 'User'

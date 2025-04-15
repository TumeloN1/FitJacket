from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goals.models import FitnessGoal
from workouts.models import WorkoutLog
from django.utils.timezone import now, timedelta
from django.db.models import Count

@login_required
def view_dashboard(request):
    first_name = request.user.username
    goals = FitnessGoal.objects.filter(user=request.user)
    logs = WorkoutLog.objects.filter(user=request.user).filter(date=now().date())
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())

    logs = WorkoutLog.objects.filter(user=request.user, date__gte=start_of_week)
    active_days = logs.values('date').distinct().count()
    chart_data = {
        'dates': [log.date.strftime('%Y-%m-%d') for log in WorkoutLog.objects.filter(user=request.user)],
        'duration': [log.duration for log in WorkoutLog.objects.filter(user=request.user)],
    }
    print(chart_data)
    return render(request, 'dashboard/dashboard.html' , {
        'first_name': first_name,
        'goals': goals,
        'logs': logs,
        'chart_data': chart_data,
        'active_days': active_days,
    })

# Create your exercise_views here.

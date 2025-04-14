from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goals.models import FitnessGoal
from workouts.models import WorkoutLog
from django.utils.timezone import now 

@login_required
def view_dashboard(request):
    first_name = request.user.username
    goals = FitnessGoal.objects.filter(user=request.user)
    logs = WorkoutLog.objects.filter(user=request.user).filter(date=now().date())
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
    })

# Create your exercise_views here.

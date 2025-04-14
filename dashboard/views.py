from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goals.models import FitnessGoal
from workouts.models import WorkoutLog

@login_required
def view_dashboard(request):
    first_name = request.user.username
    goals = FitnessGoal.objects.filter(user=request.user)
    logs = WorkoutLog.objects.filter(user=request.user).order_by('-date')[:2]
    return render(request, 'dashboard/dashboard.html' , {
        'first_name': first_name,
        'goals': goals,
        'logs': logs,
    })

# Create your exercise_views here.

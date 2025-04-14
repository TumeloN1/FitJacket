from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goals.models import FitnessGoal

@login_required
def view_dashboard(request):
    first_name = request.user.username
    goals = FitnessGoal.objects.filter(user=request.user)
    return render(request, 'dashboard/dashboard.html' , {
        'first_name': first_name,
        'goals': goals,
    })

# Create your exercise_views here.

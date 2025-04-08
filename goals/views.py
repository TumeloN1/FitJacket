from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import FitnessGoal
from .forms import FitnessGoalForm

def create_goal(request):
    if request.method == "POST":
        form = FitnessGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect("goals:view_goals")
    else:
        form = FitnessGoalForm()
    return render(request, "goals/create_goal.html", {"form": form})

def view_goals(request):
    goals = FitnessGoal.objects.filter(user=request.user)
    return render(request, "goals/view_goals.html", {"goals": goals})

@login_required
def goal_home(request):
    goals = FitnessGoal.objects.filter(user=request.user)
    return render(request, 'goals/goal_home.html', {'goals': goals})

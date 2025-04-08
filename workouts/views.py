from django.shortcuts import render, redirect
from .models import WorkoutPlan, WorkoutLog
from .forms import WorkoutLogForm
from .services.gpt_plan_generator import generate_plan
from .services.recommendation_engine import generate_recommendation
from .models import WorkoutPlan
from .services.gpt_plan_generator import generate_plan
from django.conf import settings
import requests


def view_workout_plan(request):
    plan = WorkoutPlan.objects.filter(user=request.user).last()
    if not plan:
        # Auto-generate a plan if none exists
        content = generate_plan(request.user)
        plan = WorkoutPlan.objects.create(
            user=request.user,
            name="Auto-Generated Plan",
            goal="Auto from Goal model",
            content=content
        )
    return render(request, "workouts/view_plan.html", {"plan": plan})
def log_workout(request):
    if request.method == "POST":
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect("workouts:view_plan")
    else:
        form = WorkoutLogForm()
    return render(request, "workouts/log_workout.html", {"form": form})

def recommend_workout(request):
    recs = generate_recommendation(request.user)
    return render(request, "workouts/recommendations.html", {"recommendations": recs})

def exercise_list(request):
    url = "https://exercisedb.p.rapidapi.com/exercises"
    headers = {
        "X-RapidAPI-Key": settings.EXERCISEDB_API_KEY,
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    exercises = response.json() if response.status_code == 200 else []
    return render(request, "workouts/exercise_list.html", {"exercises": exercises})
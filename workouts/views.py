from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from workouts.models import WorkoutPlan, WorkoutLog
from workouts.forms import WorkoutLogForm
from workouts.services.gpt_plan_generator import generate_plan
from workouts.services.recommendation_engine import generate_recommendation
import requests
from django.conf import settings
from FitJacket.settings import EXERCISESDB_API_KEY as exercisekey

@login_required
def view_workout_plan(request):
    plan = WorkoutPlan.objects.filter(user=request.user).last()
    if not plan:
        content = generate_plan(request.user)
        plan = WorkoutPlan.objects.create(
            user=request.user,
            name="Auto-Generated Plan",
            goal="Auto from Goal model",
            content=content
        )
        messages.success(request, "Your workout plan has been generated!")
    return render(request, "workouts/view_plan.html", {"plan": plan})

@login_required
def log_workout(request):
    if request.method == "POST":
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, "Workout log saved successfully!")
            return redirect("workouts:view_plan")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = WorkoutLogForm()
    return render(request, "workouts/log_workout.html", {"form": form})

@login_required
def edit_workout_log(request, log_id):
    log = get_object_or_404(WorkoutLog, id=log_id, user=request.user)
    if request.method == "POST":
        form = WorkoutLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, "Workout log updated successfully!")
            return redirect("workouts:view_plan")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = WorkoutLogForm(instance=log)
    return render(request, "workouts/log_workout.html", {"form": form})

@login_required
def delete_workout_log(request, log_id):
    log = get_object_or_404(WorkoutLog, id=log_id, user=request.user)
    if request.method == "POST":
        log.delete()
        messages.success(request, "Workout log deleted successfully!")
        return redirect("workouts:view_plan")
    return render(request, "workouts/confirm_delete.html", {"object": log})

@login_required
def recommend_workout(request):
    recs = generate_recommendation(request.user)
    return render(request, "workouts/recommendations.html", {"recommendations": recs})

def exercise_list(request):
    url = "https://exercisedb.p.rapidapi.com/exercises"
    headers = {
        "X-RapidAPI-Key": exercisekey,
        "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers)
        exercises = response.json() if response.status_code == 200 else []
    except Exception as e:
        exercises = []
        messages.error(request, f"Error fetching exercises: {e}")
    return render(request, "workouts/exercise_list.html", {"exercises": exercises})

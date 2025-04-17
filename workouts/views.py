from django.shortcuts import get_object_or_404
from .models import WorkoutLog
from .services.recommendation_engine import generate_recommendation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import WorkoutLogForm
from .services.gpt_plan_generator import generate_plan
from workouts.models import WorkoutPlan, SavedExercise
from django.views.decorators.http import require_POST
import json
from datetime import datetime, timedelta

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
def view_logs(request):
    logs = WorkoutLog.objects.filter(user=request.user).order_by('-date')
    return render(request, "workouts/log_home.html", {"logs": logs})

@login_required
def log_workout(request):
    if request.method == "POST":
        form = WorkoutLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, "Workout log saved successfully!")
            return redirect("workouts:view_workout", exercise=log.exercise)
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
def view_workout(request, exercise):
    # Get all logs for the same exercise
    logs = WorkoutLog.objects.filter(user=request.user, exercise=exercise).order_by('date')
    
    # Prepare chart data for all logs of the same exercise
    six_months_ago = datetime.now() - timedelta(days=6*30)  # Approximation of 6 months
    logs = logs.filter(date__gte=six_months_ago)

    chart_data = [
        [log.date.strftime('%Y-%m-%d'), log.weight] for log in logs
    ]

    return render(request, "workouts/view_workout.html", {
        "logs" : logs,
        "chart_data": json.dumps(chart_data),
        "first_name" : request.user.first_name,
        "exercise": exercise,
    })

@login_required
def recommend_workout(request):
    recs = generate_recommendation(request.user)
    return render(request, "workouts/recommendations.html", {"recommendations": recs})

@login_required
def add_exercises_home(request):
    return render(request, "workouts/add_exercises.html")

@login_required
def exercise_list(request):
    saved_qs = SavedExercise.objects.filter(user=request.user).order_by('-saved_at')

    exercises = []
    for se in saved_qs:

        secondary = getattr(se, 'secondaryMuscles', None)
        exercises.append({
            "pk": se.pk,
            "id": se.exercise_id,
            "exercise_name": se.exercise_name,
            "bodyPart": se.bodyPart,
            "target": se.target,
            "equipment": se.equipment,
            "gifUrl": se.gifUrl,
            "secondaryMuscles": secondary.split(", ") if secondary else [],
            "instructions": se.instructions.split("\n") if se.instructions else [],
        })

    return render(request, "workouts/exercise_list.html", {
        "exercises": exercises
    })

@login_required
@require_POST
def delete_saved_exercise(request, pk):
    se = get_object_or_404(SavedExercise, pk=pk, user=request.user)
    se.delete()
    messages.success(request, "Exercise removed from your library.")
    return redirect("workouts:exercise_list")
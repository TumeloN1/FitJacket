from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from goals.models import FitnessGoal
from workouts.models import WorkoutLog
from social.documents import Post, Comment  # Import your social models
from django.utils.timezone import now, timedelta
import json
from datetime import datetime
from django.db.models import Count
from collections import OrderedDict
from .models import WeightLog, Badge, Milestones
from .forms import WeightLogForm
from django.shortcuts import get_object_or_404
from django.contrib import messages


@login_required
def view_dashboard(request):
    # Fetch fitness data
    first_name = request.user.username
    goals = FitnessGoal.objects.filter(user=request.user)
    logs = WorkoutLog.objects.filter(user=request.user)
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())

    logs_today = logs.filter(date=today)
    logs_week = logs.filter(date__gte=start_of_week)
    active_days = logs_week.values('date').distinct().count()
    total_workouts = logs_week.count()
    minutes_today = 0
    for log in logs_today:
        if log.duration:
            minutes_today += log.duration.total_seconds() / 60.0

    minutes_week = {}
    for log in logs_week:
        if log.date not in minutes_week:
            minutes_week[log.date] = 0
        if log.duration:
            minutes_week[log.date] += log.duration.total_seconds() / 60.0
    minutes_week = OrderedDict(sorted(minutes_week.items()))
    # Calculate the largest increase in a single exercise from the logs in the week
    exercise_progress = {}
    for log in logs_week:
        if log.exercise not in exercise_progress:
            exercise_progress[log.exercise] = []
        exercise_progress[log.exercise].append(log.weight)

    largest_increase = 0
    for exercise, weights in exercise_progress.items():
        if len(weights) > 1:
            for i in range(len(weights) - 1):
                if weights[i + 1] - weights[i] > largest_increase:
                    largest_increase = weights[i + 1] - weights[i]

    # Fetch social feed data
    posts = Post.objects.order_by('-created_at')
    comments_by_post = {}
    for comment in Comment.objects.order_by('created_at'):
        post_key = str(comment.post.id)
        if post_key not in comments_by_post:
            comments_by_post[post_key] = []
        comments_by_post[post_key].append(comment)

    # Chart data for fitness data visualization
    chart_logs = minutes_week.items()
    chart_data = [
        [date.strftime('%Y-%m-%d'), duration] for date, duration in chart_logs
    ]
    print(chart_data)

    # Badge Checking
    milestones = Milestones.objects.all()
    active_days = WorkoutLog.objects.filter(user=request.user).values('date').distinct().count()
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('date')
    goals = [goal.goal_type for goal in FitnessGoal.objects.filter(user=request.user)]
    weight_changes = [
        weight_logs[i].weight - weight_logs[i - 1].weight
        for i in range(1, len(weight_logs))
    ]
    milestones_met = []
    for milestone in milestones:
        if milestone.target_category == "active_days" and active_days >= int(milestone.target_metric):
            milestones_met.append(milestone)
        if len(weight_changes) > 0:
            if milestone.target_category == "lose_weight" and 'lose_weight' in goals:
                if any(change < 0 and abs(change) >= int(milestone.target_metric) for change in weight_changes):
                    milestones_met.append(milestone)
            if milestone.target_category == "gain_muscle" and 'gain_muscle' in goals:
                if any(change > 0 and change >= int(milestone.target_metric) for change in weight_changes):
                    milestones_met.append(milestone)
        
    for milestone in milestones_met:
        if not Badge.objects.filter(user=request.user, milestone=milestone).exists():
            Badge.objects.create(
                user=request.user,
                name=milestone.name,
                icon="🫡",
                milestone=milestone,
            )

    user_badges = Badge.objects.filter(user=request.user)

    return render(request, 'dashboard/dashboard.html', {
        'first_name': first_name,
        'goals': goals,
        'logs': logs,
        'logs_today': logs_today,
        'logs_week': logs_week,
        'exercise': "hip thrusts",
        "chart_data": json.dumps(chart_data),
        'active_days': active_days,
        'total_workouts': total_workouts,
        'largest_increase': largest_increase,
        'posts': posts,  # Pass posts to template
        'comments_by_post': comments_by_post,  # Pass comments grouped by post to template
        'minutes_today': minutes_today,
        'user_badges': user_badges,
    })

@login_required
def log_weight(request):
    if request.method == "POST":
        form = WeightLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            messages.success(request, "Workout log saved successfully!")
            return redirect("dashboard:view_weight")
    else:
        form = WeightLogForm()
    return render(request, "dashboard/log_weight.html", {"form": form})


@login_required
def edit_weight_log(request, log_id):
    log = get_object_or_404(WeightLog, id=log_id, user=request.user)
    if request.method == "POST":
        form = WeightLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            messages.success(request, "Weight updated successfully!")
            return redirect("dashboard:view_weight")
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = WeightLogForm(instance=log)
    return render(request, "dashboard/log_weight.html", {"form": form})

@login_required
def delete_weight_log(request, log_id):
    log = get_object_or_404(WeightLog, id=log_id, user=request.user)
    if request.method == "POST":
        log.delete()
        messages.success(request, "Weight log deleted successfully!")
        return redirect("dashboard:view_weight")
    return render(request, "dashboard/confirm_delete.html", {"object": log})

@login_required
def view_weight(request):
    logs = WeightLog.objects.filter(user=request.user).order_by('date')
    six_months_ago = datetime.now() - timedelta(days=6*30)
    logs = logs.filter(date__gte=six_months_ago)
    chart_data = [
        [log.date.strftime('%Y-%m-%d'), log.weight] for log in logs
    ]
    recent_logs = WeightLog.objects.filter(user=request.user).order_by('-date')[:5]
    return render(request, "dashboard/view_weight.html", {
        "logs" : logs,
        "chart_data": json.dumps(chart_data),
        "first_name" : request.user.first_name,
        "recent_logs": recent_logs
    })
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from goals.models import FitnessGoal
from workouts.models import WorkoutLog
from social.documents import Post, Comment  # Import your social models
from django.utils.timezone import now, timedelta
import json
from datetime import datetime
from django.db.models import Count

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
    chart_logs = WorkoutLog.objects.filter(user=request.user, exercise="hip thrusts").order_by('date')
    six_months_ago = datetime.now() - timedelta(days=6*30)
    chart_logs = chart_logs.filter(date__gte=six_months_ago)
    chart_data = [
        [log.date.strftime('%Y-%m-%d'), log.weight] for log in chart_logs
    ]

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
    })

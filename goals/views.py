import markdown
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import FitnessGoal
from .forms import FitnessGoalForm
from workouts.services.gpt_plan_generator import generate_plan
from django.http import JsonResponse


@login_required
def create_goal(request):
    if request.method == "POST":
        form = FitnessGoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            # Redirect to detail view so the GPT-generated plan can be displayed
            return redirect("goals:goal_detail", goal_id=goal.id)
    else:
        form = FitnessGoalForm()
    return render(request, "goals/create_goal.html", {"form": form})

@login_required
def view_goals(request):
    goals = FitnessGoal.objects.filter(user=request.user)
    return render(request, "goals/view_goals.html", {"goals": goals})

@login_required
def goal_home(request):
    goals = FitnessGoal.objects.filter(user=request.user)
    return render(request, 'goals/goal_home.html', {'goals': goals})

@login_required
def goal_detail(request, goal_id):
    goal = get_object_or_404(FitnessGoal, id=goal_id, user=request.user)

    # Handle AJAX request for generating the plan
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Check if it's an AJAX request
        raw_plan = generate_plan(request.user, goal=goal)
        plan_html = markdown.markdown(raw_plan)
        return JsonResponse({"plan_html": plan_html})

    # Render the normal page if not an AJAX request
    return render(request, "goals/goal_detail.html", {"goal": goal})


@login_required
def update_goal(request, goal_id):
    goal = get_object_or_404(FitnessGoal, pk=goal_id, user=request.user)
    if request.method == "POST":
        form = FitnessGoalForm(request.POST, instance=goal)
        if form.is_valid():
            goal = form.save()
            return redirect("goals:goal_detail", goal_id=goal.id)
    else:
        form = FitnessGoalForm(instance=goal)
    return render(request, "goals/update_goal.html", {"form": form, "goal": goal})

@login_required
def delete_goal(request, goal_id):
    goal = get_object_or_404(FitnessGoal, pk=goal_id, user=request.user)
    if request.method == "POST":
        goal.delete()
        return redirect("goals:view_goals")
    return render(request, "goals/confirm_delete_goal.html", {"goal": goal})


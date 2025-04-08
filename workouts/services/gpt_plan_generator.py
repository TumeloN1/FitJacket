from goals.models import FitnessGoal


def generate_plan(user):
    # Get user's latest goal
    goal = FitnessGoal.objects.filter(user=user).order_by('-created_at').first()
    if not goal:
        return "No goal found. Please set a fitness goal first."

    prompt = f"Generate a personalized weekly workout plan for a user whose goal is to '{goal.description}' with a target of '{goal.target_metric}' by {goal.target_date}."

    # 🔁 Replace with actual GPT API call
    return f"Generated workout plan for goal: {goal.description}"

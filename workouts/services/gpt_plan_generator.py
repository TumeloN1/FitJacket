import openai
from FitJacket.settings import OPENAI_API_KEY
from goals.models import FitnessGoal
openai.api_key = OPENAI_API_KEY

def generate_plan(user):
    """
    Generates a personalized weekly workout plan using the OpenAI API for the given user.

    The function retrieves the user's latest fitness goal, constructs a detailed prompt using that
    goal's description, target metric, and target date, and then calls the OpenAI ChatCompletion
    endpoint to generate a workout plan.

    Parameters:
        user: The user instance for whom the plan is being generated.

    Returns:
        A string containing the generated workout plan or an error message if something goes wrong.
    """
    goal = FitnessGoal.objects.filter(user=user).order_by('-created_at').first()
    if not goal:
        return "No goal found. Please set a fitness goal first."

    target_date_str = (
        goal.target_date.strftime("%B %d, %Y")
        if hasattr(goal.target_date, "strftime")
        else str(goal.target_date)
    )

    # Construct the prompt using details from the user's fitness goal
    prompt = f"""
    You are a professional and energetic personal trainer with expertise in customizing workout plans.
    Create a detailed weekly workout plan for a client whose fitness goal is to "{goal.description}".
    The client aims to reach a target of "{goal.target_metric}" by {target_date_str}.
    Ensure the plan includes:
      - Warm-up and cool-down routines,
      - A balanced mix of cardio and strength training exercises,
      - Appropriate rest and recovery days,
      - Motivational tips and actionable advice.
    Format your response in clear, day-by-day sections.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Replace with the desired model if needed
            messages=[
                {"role": "system", "content": "You are a knowledgeable personal trainer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )

        plan = response.choices[0].message.get("content", "").strip()
        return plan if plan else "No plan generated. Please try again later."

    except Exception as e:
        return f"An error occurred generating the plan: {e}"

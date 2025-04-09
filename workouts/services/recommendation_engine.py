import openai
from FitJacket.settings import OPENAI_API_KEY
from workouts.models import WorkoutLog

openai.api_key = OPENAI_API_KEY

def generate_recommendation(user):
    """
    Generates personalized workout recommendations using OpenAI's GPT API based on the user's most recent workout log.

    Parameters:
        user: The user instance for whom the recommendations will be generated.

    Returns:
        A string containing personalized workout recommendations or an error message.
    """
    workout_log = WorkoutLog.objects.filter(user=user).order_by('-date').first()
    if not workout_log:
        return "No workout log found. Please log a workout to receive recommendations."

    summary_parts = [
        f"Date: {workout_log.date}",
        f"Exercise: {workout_log.exercise}",
        f"Sets: {workout_log.sets}",
        f"Reps: {workout_log.reps}"
    ]
    if workout_log.weight:
        summary_parts.append(f"Weight: {workout_log.weight} lbs")
    if workout_log.distance:
        summary_parts.append(f"Distance: {workout_log.distance} meters")
    if workout_log.duration:
        summary_parts.append(f"Duration: {workout_log.duration}")
    if workout_log.notes:
        summary_parts.append(f"Notes: {workout_log.notes}")

    workout_summary = ". ".join(summary_parts)

    prompt = f"""
    You are a certified fitness coach.
    A client just completed the following workout session:

    {workout_summary}

    Based on this workout, provide a personalized set of recommendations that include:
    1. Tips to improve exercise form and performance,
    2. Suggestions for complementary workouts or modifications to the routine,
    3. Advice on recovery strategies (e.g., stretching, hydration, nutrition),
    4. Motivational advice to encourage continuous progress.

    Format your response in a clear numbered list.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # Update with the model you prefer or have access to.
            messages=[
                {"role": "system", "content": "You are an expert fitness coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )

        recommendations = response.choices[0].message.get("content", "").strip()
        return recommendations if recommendations else "No recommendations were generated. Please try again."

    except Exception as e:
        return f"An error occurred while generating recommendations: {e}"

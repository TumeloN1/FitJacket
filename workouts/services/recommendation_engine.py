# workouts/services/remote_recommendation_openrouter.py

import os
import requests
from dotenv import load_dotenv
from workouts.models import WorkoutLog

load_dotenv(dotenv_path="keys.env")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in keys.env")

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}

def generate_recommendation(user):
    log = (
        WorkoutLog.objects
        .filter(user=user)
        .order_by("-date")
        .first()
    )
    if not log:
        return "No workout log found. Please log a workout to receive recommendations."

    parts = [
        f"Date: {log.date}",
        f"Exercise: {log.exercise}",
        f"Sets: {log.sets}",
        f"Reps: {log.reps}"
    ]
    if log.weight:   parts.append(f"Weight: {log.weight} lbs")
    if log.distance: parts.append(f"Distance: {log.distance} meters")
    if log.duration: parts.append(f"Duration: {log.duration}")
    if log.notes:    parts.append(f"Notes: {log.notes}")

    summary = ". ".join(parts)
    prompt = (
        "You are a certified fitness coach.\n"
        "A client just completed the following workout session:\n\n"
        f"{summary}\n\n"
        "Based on this workout, provide a personalized set of recommendations that include:\n"
        "1. Tips to improve exercise form and performance,\n"
        "2. Suggestions for complementary workouts or modifications,\n"
        "3. Advice on recovery strategies (stretching, hydration, nutrition),\n"
        "4. Motivational advice to encourage progress.\n\n"
        "Format your response in a clear numbered list.\n"
    )

    payload = {
        "model": "openrouter/tiiuae/falcon-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are an expert fitness coach."},
            {"role": "user",   "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 300,
        "top_p": 0.9,
        "repetition_penalty": 1.1
    }

    resp = requests.post(URL, headers=HEADERS, json=payload)
    if resp.status_code != 200:
        return f"Error {resp.status_code}: {resp.text}"
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()

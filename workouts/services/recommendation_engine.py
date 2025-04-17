import os
import requests
from dotenv import load_dotenv
from django.conf import settings
from workouts.models import WorkoutLog

load_dotenv(os.path.join(settings.BASE_DIR, "keys.env"))
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in keys.env")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Referer": "http://localhost:8000",
    "X-Title": "FitJacketAI",
}

def generate_recommendation(user):
    try:
        log = WorkoutLog.objects.filter(user=user).latest("date")
    except WorkoutLog.DoesNotExist:
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
    summary = "\n".join(parts)

    prompt = (
        "You are a certified fitness coach.\n"
        "A client just completed the following workout:\n\n"
        f"{summary}\n\n"
        "Based on this, provide:\n"
        "1. Form & performance tips\n"
        "2. Complementary workouts or mods\n"
        "3. Recovery strategies (stretch, hydration, nutrition)\n"
        "4. Motivational advice\n\n"
        "Format as a numbered list."
    )

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {"role": "system", "content": "You are an expert fitness coach."},
            {"role": "user",   "content": prompt},
        ],
        "temperature": 0.8,
        "max_tokens": 500,
        "top_p": 0.9,
        "repetition_penalty": 1.1,
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    try:
        msg = response.json()["choices"][0]["message"]
        content = msg.get("content") or msg.get("reasoning") or ""
    except Exception as e:
        return f"Unexpected API response format: {e}\n\n{response.text}"

    if not content:
        return f"No text returned by model. Raw response:\n\n{response.text}"

    return content.strip()

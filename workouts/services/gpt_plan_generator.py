
import os
import requests
from dotenv import load_dotenv
from goals.models import FitnessGoal

load_dotenv(dotenv_path="keys.env")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set in keys.env")

URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {OPENROUTER_API_KEY}"}

def generate_plan(user):
    goal = (
        FitnessGoal.objects
        .filter(user=user)
        .order_by("-created_at")
        .first()
    )
    if not goal:
        return "No goal found. Please set a fitness goal first."

    date_str = goal.target_date.strftime("%B %d, %Y")
    prompt = (
        "You are a professional and energetic personal trainer with expertise in customizing workout plans.\n"
        f"Create a detailed weekly workout plan for a client whose fitness goal is \"{goal.description}\".\n"
        f"The client aims to reach a target of \"{goal.target_metric}\" by {date_str}.\n"
        "Ensure the plan includes:\n"
        "  - Warm-up and cool-down routines,\n"
        "  - A balanced mix of cardio and strength training exercises,\n"
        "  - Appropriate rest and recovery days,\n"
        "  - Motivational tips and actionable advice.\n"
        "Format your response in clear, day-by-day sections.\n\n"
        "Plan:\n"
    )

    payload = {
        "model": "openrouter/tiiuae/falcon-7b-instruct",
        "messages": [
            {"role": "system", "content": "You are a knowledgeable personal trainer."},
            {"role": "user",   "content": prompt}
        ],
        "temperature": 0.8,
        "max_tokens": 500,
        "top_p": 0.9,
        "repetition_penalty": 1.1
    }

    resp = requests.post(URL, headers=HEADERS, json=payload)
    if resp.status_code != 200:
        return f"Error {resp.status_code}: {resp.text}"
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()

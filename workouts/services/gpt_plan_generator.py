import os
import requests
from dotenv import load_dotenv
from django.conf import settings
from datetime import date
from goals.models import FitnessGoal

# ── Setup ─────────────────────────────────────────────────────────
dotenv_path = os.path.join(settings.BASE_DIR, "keys.env")
load_dotenv(dotenv_path=dotenv_path)
API_KEY = os.getenv("OPENROUTER_API_KEY")
if not API_KEY:
    raise ValueError("OPENROUTER_API_KEY not set")

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Referer": "http://localhost:8000",
    "X-Title": "FitJacketAI",
}

# Local lists
EQUIP_URL     = "http://127.0.0.1:8000/workouts/api/exercises/equipmentlist/"
BODYPARTS_URL = "http://127.0.0.1:8000/workouts/api/exercises/bodyparts/"
LIBRARY_URL   = "http://127.0.0.1:8000/workouts/exercises/"

def generate_plan(user, goal=None, workout_type="gym"):
    # 1) Resolve or fail on goal
    if not goal:
        try:
            goal = FitnessGoal.objects.filter(user=user).latest("created_at")
        except FitnessGoal.DoesNotExist:
            return "No goal found. Please set one first."

    today = date.today().strftime("%B %d, %Y")
    target = goal.target_date.strftime("%B %d, %Y")

    try: equips = requests.get(EQUIP_URL).json()[:5]
    except: equips = []
    try: bodies= requests.get(BODYPARTS_URL).json()[:5]
    except: bodies = []

    # 3) Build prompt
    hw_type = "Home" if workout_type=="home" else "Gym"
    equip_txt = ", ".join(equips) or "bodyweight/barbell movements"
    body_txt  = ", ".join(bodies) or "major muscle groups"

    prompt = (
        f"# 8‑Week {hw_type} Workout Plan (Generated {today})\n\n"
        f"**Goal:** {goal.description} (target {goal.target_metric} by {target})\n"
        f"**Type:** {hw_type}\n\n"
        f"Use equipment like: {equip_txt}. Target: {body_txt}.\n\n"
        "Give me a concise **weekly** overview for 8 weeks. For **each week**, outline:\n"
        "1. **Main focus** (e.g., Lower-body split, upper-body split, arms day, chest and back day)\n"
        "2. **3–5 key sessions** (e.g., Barbell Squat, Bench Press, just use some of the equipment and target groups given)\n"
        "3. **Rest/recovery recommendations**\n"
        "4. **Motivational tip**\n\n"
        "Format in Markdown with `## Week 1`, `## Week 2`, … through `## Week 8`.\n\n"
        "Plan:\n"
    )

    payload = {
        "model": "deepseek/deepseek-r1:free",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a professional personal trainer. "
                    "Provide only the workout plan in Markdown format, with no reasoning or internal thoughts. "
                    "Use headings for each week (e.g. ## Week 1), bold for exercise names, and lists for sets/reps."
                )
            },
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1200,
        "top_p": 0.9,
        "repetition_penalty": 1.1,
    }

    resp = requests.post(API_URL, headers=HEADERS, json=payload)
    if resp.status_code != 200:
        return f"Error {resp.status_code}: {resp.text}"

    # parse ONLY the content field
    data = resp.json().get("choices", [{}])[0].get("message", {})
    content = data.get("content", "").strip()
    if not content:
        return f"No plan returned (raw):\n{resp.text}"

    # append your library link and return
    return content + f"\n\n—\nBrowse more exercises: [Exercise Library]({LIBRARY_URL})"

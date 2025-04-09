import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

BASE_URL = "https://exercisedb.p.rapidapi.com"

def _make_exercise_request(endpoint: str):
    """
    Internal helper to DRY up the request logic.
    `endpoint`: string (e.g. "/exercises" or "/exercises/bodyPartList")
    Returns the parsed JSON on success, or None if there's an error.
    """
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "X-RapidAPI-Key": getattr(settings, "EXERCISEDB_API_KEY", ""),
        "X-RapidAPI-Host": getattr(settings, "EXERCISEDB_API_HOST", "exercisedb.p.rapidapi.com"),
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def browse_exercises(request):
    """
    Renders a single-page template containing multiple "tabs" or sections:
    - All Exercises
    - Filter by Body Part
    - Filter by Equipment
    - Filter by Target
    - Search by Name
    Clicking each tab or button triggers AJAX calls to our internal endpoints that fetch data from the ExerciseDB API.
    """
    return render(request, "workouts/exercise_browse.html")

def api_exercises_list(request):
    """ Returns the full list of exercises. """
    data = _make_exercise_request("/exercises")
    if data is None:
        return JsonResponse({"error": "Unable to fetch exercises."}, status=500)
    return JsonResponse(data, safe=False)

def api_bodypart_list(request):
    """ Returns the list of available body parts. """
    data = _make_exercise_request("/exercises/bodyPartList")
    if data is None:
        return JsonResponse({"error": "Unable to fetch body part list."}, status=500)
    return JsonResponse(data, safe=False)

def api_equipment_list(request):
    """ Returns the list of available equipment. """
    data = _make_exercise_request("/exercises/equipmentList")
    if data is None:
        return JsonResponse({"error": "Unable to fetch equipment list."}, status=500)
    return JsonResponse(data, safe=False)

def api_target_list(request):
    """ Returns the list of available target muscle groups. """
    data = _make_exercise_request("/exercises/targetList")
    if data is None:
        return JsonResponse({"error": "Unable to fetch target list."}, status=500)
    return JsonResponse(data, safe=False)

def api_exercises_by_bodypart(request, bodypart):
    """ Returns exercises filtered by a specific body part. """
    endpoint = f"/exercises/bodyPart/{bodypart}"
    data = _make_exercise_request(endpoint)
    if data is None:
        return JsonResponse({"error": f"Unable to fetch exercises for {bodypart}."}, status=500)
    return JsonResponse(data, safe=False)

def api_exercises_by_equipment(request, equipment):
    """ Returns exercises filtered by a specific equipment. """
    endpoint = f"/exercises/equipment/{equipment}"
    data = _make_exercise_request(endpoint)
    if data is None:
        return JsonResponse({"error": f"Unable to fetch exercises for {equipment}."}, status=500)
    return JsonResponse(data, safe=False)

def api_exercises_by_target(request, target):
    """ Returns exercises filtered by a specific target muscle. """
    endpoint = f"/exercises/target/{target}"
    data = _make_exercise_request(endpoint)
    if data is None:
        return JsonResponse({"error": f"Unable to fetch exercises for target {target}."}, status=500)
    return JsonResponse(data, safe=False)

def api_exercises_by_name(request, name):
    """ Returns exercises matching the given name. """
    endpoint = f"/exercises/name/{name}"
    data = _make_exercise_request(endpoint)
    if data is None:
        return JsonResponse({"error": f"Unable to fetch exercises for name {name}."}, status=500)
    return JsonResponse(data, safe=False)

def api_exercise_detail(request, exercise_id):
    """ Returns details for a single exercise by ID. """
    endpoint = f"/exercises/exercise/{exercise_id}"
    data = _make_exercise_request(endpoint)
    if data is None:
        return JsonResponse({"error": f"Unable to fetch exercise ID {exercise_id}."}, status=500)
    return JsonResponse(data, safe=False)

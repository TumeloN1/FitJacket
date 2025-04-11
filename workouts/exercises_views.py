import logging, requests
from email.utils import unquote
from urllib.parse import quote
from datetime import datetime
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from pymongo import MongoClient
from workouts.models import SavedExercise

logger = logging.getLogger(__name__)

BASE_URL = "https://exercisedb.p.rapidapi.com"
API_KEY  = "0c352b3043mshb17b79077c49065p1370f9jsnfc01abd2f695"
API_HOST = "exercisedb.p.rapidapi.com"

def _make_exercise_request(path: str):
    url = f"{BASE_URL}{path}"
    headers = {
        "X-RapidAPI-Key":  API_KEY,
        "X-RapidAPI-Host": API_HOST,
    }
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json(), resp.status_code
    except requests.RequestException as e:
        status = getattr(e.response, "status_code", 502)
        logger.error("API error on %s: %s", url, e, exc_info=True)
        return None, status

def get_mongo_collection():
    uri = getattr(settings, "MONGO_ATLAS_URI", None)
    name = getattr(settings, "MONGO_DB_NAME", None)
    if not uri or not name:
        raise ImproperlyConfigured("MONGO_ATLAS_URI and MONGO_DB_NAME must be set in settings")
    client = MongoClient(uri)
    return client[name]["exercise_cache"]

cache_col = get_mongo_collection()

def get_from_cache(category, key):
    doc = cache_col.find_one({"category": category, "key": key})
    return doc["data"] if doc else None


def store_in_cache(category, key, data):
    cache_col.update_one(
        {"category": category, "key": key},
        {"$set": {"data": data, "cached_at": datetime.utcnow()}},
        upsert=True
    )


def ensure_cache_category(category, list_path, item_path_tpl):
    """
    1) Fetch the list (bodyPartList / equipmentList / targetList).
    2) For each item, if not already cached, fetch /exercises/<category>/<item>/ and cache it.
    """
    items, status = _make_exercise_request(list_path)
    if not items:
        logger.error("Unable to fetch %s list for caching", category)
        return
    for item in items:
        if not get_from_cache(category, item):
            data, st = _make_exercise_request(item_path_tpl.format(item=quote(item)))
            if data:
                store_in_cache(category, item, data)

# ── Views ────────────────────────────────────────────────────────────────────

@login_required
def browse_exercises(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return render(request, "workouts/exercise_browse.html")

@login_required
def api_exercises_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    data, status = _make_exercise_request("/exercises")
    if data is None:
        return JsonResponse({"error": "Unable to fetch exercises."}, status=status)
    fmt = request.GET.get("format")
    accept = request.META.get("HTTP_ACCEPT", "")
    if fmt == "html" or ("text/html" in accept and "application/json" not in accept):
        return render(request, "workouts/exercise_list.html", {"exercises": data})
    return JsonResponse(data, safe=False, status=status)

@login_required
def api_bodypart_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    ensure_cache_category("bodyPart", "/exercises/bodyPartList", "/exercises/bodyPart/{item}")
    data, status = _make_exercise_request("/exercises/bodyPartList")
    return JsonResponse(data or [], safe=False, status=status)

@login_required
def api_equipment_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    ensure_cache_category("equipment", "/exercises/equipmentList", "/exercises/equipment/{item}")
    data, status = _make_exercise_request("/exercises/equipmentList")
    return JsonResponse(data or [], safe=False, status=status)

@login_required
def api_target_list(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    ensure_cache_category(
        "target",
        "/exercises/targetList",
        "/exercises/target/{item}"
    )

    targets, status = _make_exercise_request("/exercises/targetList")
    if targets is None:
        return JsonResponse(
            {"error": "Unable to fetch target list.", "status": status},
            status=status
        )

    exercises_by_target = {
        t: get_from_cache("target", t) or []
        for t in targets
    }

    return JsonResponse({
        "targets": targets,
        "exercises": exercises_by_target
    }, status=status)

@login_required
def api_exercises_by_bodypart(request, bodypart):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    cached = get_from_cache("bodyPart", bodypart)
    if cached is not None:
        return JsonResponse(cached, safe=False)
    data, status = _make_exercise_request(f"/exercises/bodyPart/{quote(bodypart)}")
    if data:
        store_in_cache("bodyPart", bodypart, data)
        return JsonResponse(data, safe=False, status=status)
    return JsonResponse({"error": "Not found"}, status=status)

@login_required
def api_exercises_by_equipment(request, equipment):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    cached = get_from_cache("equipment", equipment)
    if cached is not None:
        return JsonResponse(cached, safe=False)
    data, status = _make_exercise_request(f"/exercises/equipment/{quote(equipment)}")
    if data:
        store_in_cache("equipment", equipment, data)
        return JsonResponse(data, safe=False, status=status)
    return JsonResponse({"error": "Not found"}, status=status)

@login_required
def api_exercises_by_target(request, target):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    cached = get_from_cache("target", target)
    if cached is not None:
        return JsonResponse(cached, safe=False)
    data, status = _make_exercise_request(f"/exercises/target/{quote(target)}")
    if data:
        store_in_cache("target", target, data)
        return JsonResponse(data, safe=False, status=status)
    return JsonResponse({"error": "Not found"}, status=status)


@login_required
def cache_dump_html(request):
    categories = cache_col.distinct("category")
    dump = {}
    for cat in categories:
        docs = cache_col.find({"category": cat}, {"key": 1, "_id": 0})
        dump[cat] = [d["key"] for d in docs]
    return render(request, "workouts/cache_dump.html", {"cache": dump})

@login_required
def bodypart_browse_view(request):
    return render(request, "workouts/bodyPart_browse.html")

@login_required
def target_browse_view(request):
    return render(request, "workouts/targetMuscle_browse.html")

@login_required
def equipment_browse_view(request):
    return render(request, "workouts/equipment_browse.html")


@login_required
def exercise_detail_view(request, exercise_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    eid = quote(unquote(exercise_id))

    cached = get_from_cache("exercise", eid)
    if cached is not None:
        exercise = cached
    else:
        data, status = _make_exercise_request(f"/exercises/exercise/{eid}")
        if data is None:
            return JsonResponse({"error": "Unable to fetch exercise."}, status=status)
        exercise = data
        store_in_cache("exercise", eid, exercise)

    if not exercise.get("id"):
        return JsonResponse({"error": "Exercise not found."}, status=404)

    return render(request, "workouts/exercise_detail.html", {"exercise": exercise})


@login_required
@require_POST
def save_exercise_view(request, exercise_id):
    eid = quote(unquote(exercise_id))
    cached = get_from_cache("exercise", eid)
    if cached is not None:
        exercise = cached
    else:
        data, status = _make_exercise_request(f"/exercises/exercise/{eid}")
        if data is None:
            return JsonResponse({"error": "Unable to fetch exercise."}, status=status)
        exercise = data
        store_in_cache("exercise", eid, exercise)

    if not exercise.get("id"):
        return JsonResponse({"error": "Exercise not found."}, status=404)

    saved, created = SavedExercise.objects.get_or_create(
        user=request.user,
        exercise_id=exercise["id"],
        defaults={
            "exercise_name": exercise.get("exercise_name", ""),
            "bodyPart": exercise.get("bodyPart", ""),
            "target": exercise.get("target", ""),
            "equipment": exercise.get("equipment", ""),
            "secondaryMuscles": exercise.get("secondaryMuscles", ""),
            "gifUrl": exercise.get("gifUrl", ""),
            "instructions": "\n".join(exercise.get("instructions", [])),
        }
    )
    if created:
        messages.success(request, "Exercise saved successfully!")
    else:
        messages.info(request, "This exercise is already in your library.")

    return redirect("workouts:exercise_list")
from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from django.urls import include

app_name = "dashboard"

urlpatterns = [
    path('', login_required(views.view_dashboard), name="view_dashboard"),
]
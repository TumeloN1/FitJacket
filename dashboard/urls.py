from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
from django.urls import include

app_name = "dashboard"

urlpatterns = [
    path('', login_required(views.view_dashboard), name="view_dashboard"),
    path('log/create', login_required(views.log_weight), name="log_weight"),
    path('log/edit/<int:log_id>/', login_required(views.edit_weight_log), name="edit_weight_log"),
    path('log/delete/<int:log_id>/', login_required(views.delete_weight_log), name="delete_weight_log"),
    path('log/view',login_required(views.view_weight), name="view_weight")
]
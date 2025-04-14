from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def view_dashboard(request):
    first_name = request.user.username
    return render(request, 'dashboard/dashboard.html' , {'first_name': first_name})

# Create your exercise_views here.

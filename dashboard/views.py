from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def view_dashboard(request):
    return render(request, 'dashboard/dashboard.html')

# Create your exercise_views here.

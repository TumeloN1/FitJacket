from django import forms
from .models import WorkoutLog

class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ["date", "exercise", "sets", "reps", "weight", "distance", "duration", "notes"]

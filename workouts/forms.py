from django import forms
from .models import WorkoutLog
from django.utils.timezone import now

class WorkoutLogForm(forms.ModelForm):
    class Meta:
        model = WorkoutLog
        fields = ["date", "exercise", "sets", "reps", "weight", "distance", "duration", "notes"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = now().date
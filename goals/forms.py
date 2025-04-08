from django import forms
from .models import FitnessGoal

class FitnessGoalForm(forms.ModelForm):
    class Meta:
        model = FitnessGoal
        fields = ["goal_type", "description", "target_metric", "target_date"]
        widgets = {
            "target_date": forms.DateInput(attrs={"type": "date"}),
        }

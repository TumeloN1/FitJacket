from django import forms
from .models import FitnessGoal

class FitnessGoalForm(forms.ModelForm):
    class Meta:
        model = FitnessGoal
        fields = [
            "goal_type",
            "description",
            "target_metric",
            "target_date",
        ]
        widgets = {
            "target_date": forms.DateInput(attrs={"type": "date"})
        }

class GoalSelectionForm(forms.Form):
    goal = forms.ModelChoiceField(
        queryset=FitnessGoal.objects.none(),
        label="Select Goal",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["goal"].queryset = (
            FitnessGoal.objects
            .filter(user=user)
            .order_by("-created_at")
        )
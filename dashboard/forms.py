from django import forms
from .models import WeightLog
from django.utils.timezone import now

class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ["date", "weight", "notes"]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].initial = now().date
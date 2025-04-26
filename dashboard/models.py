from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} – {self.weight} on {self.date}"

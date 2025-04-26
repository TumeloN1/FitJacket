from django.db import models
from django.contrib.auth import get_user_model
from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, CASCADE
from datetime import datetime

User = get_user_model()

class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    weight = models.FloatField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} – {self.weight} on {self.date}"


# Milestone condition to award badge
class Milestones(models.Model):
    CATEGORIES = [
        ("lose_weight", "Lose Weight"),
        ("gain_muscle", "Gain Muscle"),
        ("active_days", "Active Days"),
    ]
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    target_category = models.CharField(max_length=50, choices=CATEGORIES)
    target_metric = models.CharField(max_length=20)
    def __str__(self):
        return self.name

# Badge itself
class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    milestone = models.ForeignKey(Milestones, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
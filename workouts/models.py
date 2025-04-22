from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class WorkoutPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    goal = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.user.username} – {self.name}"

class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    exercise = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField(blank=True, null=True)
    distance = models.FloatField(blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} – {self.exercise} on {self.date}"

class SavedExercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise_id = models.CharField(max_length=20)
    exercise_name = models.CharField(max_length=200)
    bodyPart = models.CharField(max_length=200)
    target = models.CharField(max_length=200)
    equipment = models.CharField(max_length=200)
    secondaryMuscles = models.TextField(blank=True, default='')
    gifUrl = models.URLField()
    instructions = models.TextField()
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exercise_name} (saved by {self.user.username})"

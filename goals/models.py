from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class FitnessGoal(models.Model):
    GOAL_TYPES = [
        ("lose_weight", "Lose Weight"),
        ("gain_muscle", "Gain Muscle"),
        ("improve_endurance", "Improve Endurance"),
        ("general_health", "General Health"),
    ]

    IMAGE_PATHS = [
        ("lose_weight", "img/excercise.png"),
        ("gain_muscle", "img/muscle.png"),
        ("improve_endurance", "img/stopwatch.png"),
        ("general_health", "img/cardiogram.png"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50, choices=GOAL_TYPES)
    description = models.TextField()
    target_metric = models.CharField(max_length=100)
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.description} by {self.target_date}"

    def get_image_path(self):
        image_dict = dict(self.IMAGE_PATHS)
        return image_dict.get(self.goal_type, "img/default.png")
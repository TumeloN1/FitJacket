from django.db import models
from django.contrib.auth import get_user_model

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=50, choices=GOAL_TYPES)
    description = models.TextField()
    target_metric = models.CharField(max_length=100, help_text="E.g. 'Lose 10 lbs' or 'Run 5K under 25 mins'")
    target_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_goal_type_display()}"

    def get_image_path(self):
        image_dict = dict(self.IMAGE_PATHS)
        return image_dict.get(self.goal_type, "img/default.png")
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

class Milestones(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    target = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="badges/icons", blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    milestone = models.ForeignKey(Milestones, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, CASCADE
from accounts.documents import Account  # Import the Account model here
from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

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

# Post model (user or group post)
class Post(Document):
    author = ReferenceField(Account, required=True)  # Use the Account model to represent the author
    content = StringField(required=True)  # Content of the post
    created_at = DateTimeField(default=datetime.utcnow)
    likes = ListField(ReferenceField(Account))  # List of users who liked the post (references Account model)
    group = ReferenceField('Group', null=True)  # Group reference, if post is related to a group

# Comment model (for commenting on posts)
class Comment(Document):
    content = StringField(required=True, max_length=500)
    author = ReferenceField(Account, required=True, reverse_delete_rule=CASCADE)  # Use Account as the author
    post = ReferenceField(Post, required=True, reverse_delete_rule=CASCADE)  # The post being commented on
    created_at = DateTimeField(default=datetime.utcnow)

# Group model (for creating and managing groups)
class Group(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    members = ListField(ReferenceField(Account))  # List of members in the group
    admins = ListField(ReferenceField(Account))   # List of group admins
    created_at = DateTimeField(default=datetime.utcnow)

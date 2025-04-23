from mongoengine import Document, StringField, ListField, ReferenceField, DateTimeField, CASCADE
from accounts.documents import Account  # Import the Account model here
from datetime import datetime

# Post model (user or group post)
class Post(Document):
    author = ReferenceField(Account, required=True)  # Use the Account model to represent the author
    content = StringField(required=True)  # Content of the post
    created_at = DateTimeField(default=datetime.utcnow)
    likes = ListField(ReferenceField(Account))  # List of users who liked the post (references Account model)
    group = ReferenceField('Group', null=True)  # Group reference, if post is related to a group
    meta = {
        'collection': 'posts'
    }

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

class Friendship(Document):
    user = ReferenceField(Account, required=True, reverse_delete_rule=2)  # 2 means CASCADE delete
    friend = ReferenceField(Account, required=True, reverse_delete_rule=2)
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'friendships',
        'indexes': [
            {'fields': ['user', 'friend'], 'unique': True}  # Ensure friendships are unique
        ]
    }

    def __str__(self):
        return f"{self.user.username} is friends with {self.friend.username}"

class FriendRequest(Document):
    sender = ReferenceField(Account, required=True)
    receiver = ReferenceField(Account, required=True)
    status = StringField(choices=['pending', 'accepted', 'rejected'], default='pending')
    created_at = DateTimeField(default=datetime.utcnow)

    meta = {
        'collection': 'friend_requests'
    }
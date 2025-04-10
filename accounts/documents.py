import datetime
from mongoengine import Document, StringField, EmailField, DateTimeField

class Account(Document):
    username = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)
    password_hash = StringField(required=True)  # Store a hashed password
    first_name = StringField(max_length=30, required=True)
    last_name = StringField(max_length=30, required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)

    meta = {
        'collection': 'accounts'
    }

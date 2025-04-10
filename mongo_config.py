from mongoengine import connect
from django.conf import settings

def connect_to_mongo():
    connect(
        db=settings.MONGO_DB_NAME,
        host=settings.MONGO_ATLAS_URI
    )

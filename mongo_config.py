import mongoengine
from django.conf import settings

def connect_to_mongo():
    mongoengine.connect(
        db=settings.MONGO_DB_NAME,
        host=settings.MONGO_HOST,
        port=settings.MONGO_PORT,
        username=settings.MONGO_USERNAME or None,
        password=settings.MONGO_PASSWORD or None,
        authentication_source=settings.MONGO_AUTH_SOURCE
    )

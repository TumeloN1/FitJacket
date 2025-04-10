from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .documents import Account

class MongoEngineBackend(BaseBackend):
    """
    Authenticate against MongoEngine Account, then return (or create)
    a corresponding Django User.
    """
    def authenticate(self, request, username=None, password=None):
        if not username or not password:
            return None

        # lookup Account by email or username
        if '@' in username:
            acct = Account.objects(email=username).first()
        else:
            acct = Account.objects(username=username).first()
        if not acct or not check_password(password, acct.password_hash):
            return None

        user, created = User.objects.get_or_create(
            username=acct.username,
            defaults={
                'email': acct.email,
                'first_name': acct.first_name,
                'last_name': acct.last_name,
            }
        )
        if created:
            user.set_unusable_password()
            user.save()
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

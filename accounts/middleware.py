from django.contrib.auth.models import AnonymousUser
from django.utils.functional import SimpleLazyObject
from .documents import Account

def get_mongo_user(request):
    account_id = request.session.get('account_id')
    if account_id:
        try:
            acct = Account.objects.get(id=account_id)
            setattr(acct, 'is_authenticated', True)
            return acct
        except Account.DoesNotExist:
            pass
    return AnonymousUser()

class MongoEngineAuthMiddleware:
    """
    After Django's AuthenticationMiddleware, overwrite request.user
    with your MongoEngine Account (if present in session).
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user = SimpleLazyObject(lambda: get_mongo_user(request))
        return self.get_response(request)

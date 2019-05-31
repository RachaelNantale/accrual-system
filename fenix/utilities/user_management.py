import jwt
from django.conf import settings
from rest_framework.exceptions import NotFound

from fenix.system.models import User


def get_id_from_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    payload = jwt.decode(token, settings.SECRET_KEY, 'utf-8')
    return payload['id'], payload['username']


def getUserFromDatabase(pk=0, username=""):
    """Get user from the database by id or username"""
    if User.objects.filter(pk=pk).exists():
        return User.objects.get(pk=pk)
    elif User.objects.filter(username=username).exists():
        return User.objects.get(username=username)
    else:
        raise NotFound(detail="User Not found")

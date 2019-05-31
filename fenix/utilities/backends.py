import jwt

from django.conf import settings

from rest_framework import authentication, exceptions

from fenix.system.models import User


class JWTAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """
        This method is called for on every request and it
        returns a two-tuple of (user, token) if authentication is
        successfull and a None otherwise.
        If any fails we raise `AuthenticationFailed` and Django rest framework
        does the rest.
        """
        authentication_header_prefix = 'Token'
        request.user = None

        authentication_header = authentication.get_authorization_header(
            request).split()

        if not authentication_header:
            return None
        prefix = authentication_header[0].decode('utf-8')
        token = authentication_header[1].decode('utf-8')

        if prefix != authentication_header_prefix:
            return None
        return self.authenticate_user_details(token)

    def authenticate_user_details(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
        except Exception:
            raise exceptions.AuthenticationFailed('Invalid/expired token')

        user = User.objects.get(pk=payload['id'])
        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'User is currently either inactive or deleted')

        return (user, token)

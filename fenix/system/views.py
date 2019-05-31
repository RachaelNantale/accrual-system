from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import (RegisterSerializer, LoginSerializer)

from .models import User
from .renderers import UserJSONRenderer


class RegisterListUserView(generics.ListCreateAPIView):
    """This creates a new user"""
    permission_classes = ()
    authentication_classes = ()
    renderer_classes = (UserJSONRenderer, )
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class LoginView(generics.CreateAPIView):
    """The Login view creates an interface
     where the user can login and
    get a token for authentication"""
    permission_classes = ()
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import (RegisterSerializer, LoginSerializer,
                          RequestPointsSerializer, ProfileSerializer)

from .models import User, RequestPoints, Profile
from .renderers import UserJSONRenderer, GeneralRenderer
from fenix.utilities.exceptions import UserCannotEditProfile
from fenix.utilities.user_management import (get_id_from_token,
                                             getUserFromDatabase)


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


class RequestPointsView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = RequestPointsSerializer
    renderer_classes = (GeneralRenderer, )
    queryset = RequestPoints.objects.all()

    def post(self, request, username, *args, **kwargs):
        user_requesting = getUserFromDatabase(username=username)
        current_user_id, current_username = get_id_from_token(request)
        request_data = {
            "owner": current_user_id,
            "status": request.data.get('status')
        }
        serializer = serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Allow users  to retrieve and edit their profiles
    Params: username: A username is needed in order to get a specific profile.
    """
    permission_classes = (IsAuthenticated, )
    renderer_classes = (GeneralRenderer, )
    serializer_class = ProfileSerializer

    def get(self, request, username, *args, **kwargs):
        user = getUserFromDatabase(username=username)
        serializer = self.serializer_class(user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username, *args, **kwargs):
        serializer_data = request.data.get('profiles', {})
        user = getUserFromDatabase(username=username)

        try:
            user_id, username, = get_id_from_token(request)
            if user.username != username:
                raise UserCannotEditProfile
        except Exception:
            raise UserCannotEditProfile

        serializer_data = {
            'first_name': serializer_data.get('first_name', request.user.profile.last_name),
            'last_name': serializer_data.get('last_name', request.user.profile.last_name),
            'seniority': serializer_data.get('seniority', request.user.profile.seniority),
            'tenure': serializer_data.get('tenure', request.user.profile.tenure),
            'points_balance': serializer_data.get('points_balance', request.user.profile.points_balance)
        }
        serializer = self.serializer_class(
            request.user.profile,
            data=serializer_data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user.profile, serializer_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileListAPIView(generics.ListAPIView):
    """Allow user to view other user profiles"""
    permission_classes = (IsAdminUser, )
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

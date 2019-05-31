from django.urls import path

from .views import (RegisterListUserView, LoginView,
                    ProfileRetrieveUpdateAPIView, ProfileListAPIView)


urlpatterns = [
    path('api/users', RegisterListUserView.as_view(), name='register'),
    path("api/login", LoginView.as_view(), name="login"),
    path('api/profiles/<username>',
         ProfileRetrieveUpdateAPIView.as_view(), name='profile'),
    path('api/profiles', ProfileListAPIView.as_view(), name='profile_list'),

]

from django.urls import path

from .views import (RegisterListUserView, LoginView)


urlpatterns = [
    path('api/users', RegisterListUserView.as_view(), name='register'),
    path("api/login", LoginView.as_view(), name="login"),
]

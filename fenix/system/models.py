import jwt
import time
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.conf import settings


class UserManager(BaseUserManager):
    """Create models for the user"""

    def create_user(self, username, email, profile, password=None):
        user = self.model(
            username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        user.profile = profile
        user.profile.save()
        return user

    def create_superuser(self, username, email, profile, password):
        """ Create a user with admin rights"""
        if password is None:
            raise TypeError('Admins must have a password')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        user.profile = profile
        user.profile.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ This class describes the fields of the User"""
    username = models.CharField(db_index=True, max_length=255, unique=True)
    last_name = models.CharField(blank=True, max_length=50)
    first_name = models.CharField(blank=True, max_length=50)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'profile']

    objects = UserManager()

    def __str__(self):
        """Return a string representation of the user"""
        return self.email

    class Meta:
        ordering = ('username',)

    def _generate_jwt_token(self):
        """
        Generates the token that stores the user's id
        It also expires in 2 days
        """
        token = jwt.encode({
            'id': self.pk,
            'username': self.username,
            'email': self.email,
            'exp': 1609416000
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    @property
    def token(self):
        return self._generate_jwt_token()


class Profile(models.Model):
    """Defines the  descriptive data for the different user profiles created"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    date_joined = models.DateTimeField(auto_now=False, default=timezone.now)
    points_balance = models.IntegerField(default=0, null=False, blank=False)
    seniority = models.CharField(blank=True, max_length=5)


class RequestPoints(models.Model):
    PENDING = 'pending'
    ACTIVE = 'active'
    DELIVERED = 'delivered'
    STATUS_CHOICES = ((PENDING, 'pending'),
                      (ACTIVE, 'active'), (DELIVERED, 'delivered'),)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    number_of_points = models.IntegerField(default=0)
    request_reason = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status

    class Meta:
        ordering = ('status',)

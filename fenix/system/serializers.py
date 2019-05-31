from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User
from fenix.utilities.custom_validators import ValidateUserData


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for registering a new user"""
    password = serializers.CharField(max_length=128,
                                     min_length=8,
                                     write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)

        validator = ValidateUserData()
        validator.register_validation(username, email, password)
        return {'email': email, 'username': username, 'password': password}

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'token']
        read_only_fields = ('token', )


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.')
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.')
        user = authenticate(username=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }

    class Meta:
        model = User
        fields = ['email', 'username', 'token']
        read_only_fields = ('token',)

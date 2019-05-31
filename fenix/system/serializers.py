from django.contrib.auth import authenticate
from rest_framework import serializers, status
from rest_framework.response import Response
from datetime import datetime, timezone

from .models import User, RequestPoints, Profile
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

    def create(self, validated_data):
        profile = Profile()
        return User.objects.create_user(**validated_data, profile=profile)


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


class RequestPointsSerializer(serializers.HyperlinkedModelSerializer):
    """Class for creating a nd withdrawing requests for points"""
    owner = serializers.ReadOnlyField()

    class Meta:
        model = RequestPoints
        fields = ('id', 'number_of_points', 'owner', 'status',
                  'created_at', 'updated_at')

        read_only_fields = ('owner',)


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for creating a profile"""
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.CharField(allow_blank=True, required=False,
                                       min_length=2, max_length=50)
    last_name = serializers.CharField(allow_blank=True, required=False,
                                      min_length=2,
                                      max_length=50)
    tenure = serializers.SerializerMethodField(source='tenure')
    date_joined = serializers.DateTimeField(
        format="%d-%m-%Y", input_formats=['%d-%m-%Y'])

    def validate(self, data):
        first_name = data.get('first_name', None)
        last_name = data.get("last_name", None)
        date_joined = data.get('date_joined', None)
        seniority = data.get('seniority', None)
        tenure = data.get('tenure', None)
        points_balance = data.get('points_balance', None)

        return {'first_name': first_name, 'last_name': last_name,
                'date_joined': date_joined, 'seniority': seniority,
                'tenure': tenure, 'points_balance': points_balance}

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name',
                  'date_joined', 'seniority', 'tenure', 'points_balance']
        read_only_fields = ('username', 'points_balance', 'tenure', )

    def get_tenure(self, obj):
        """
        A function that returns the tenure of an employee.
        It takes in the current time  and substracts the
        time when the employee joined.
        This field(tenure) is not part of the model
        """
        return (datetime.now(timezone.utc) - obj.date_joined).days / 365.25

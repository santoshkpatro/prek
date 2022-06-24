from rest_framework import serializers
from prek.models.user import User


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'email',
            'full_name',
            'phone',
            'profile_url'
        ]


class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    full_name = serializers.CharField()
    password = serializers.CharField()


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

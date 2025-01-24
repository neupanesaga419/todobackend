from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from custom_auth.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name"]


class UserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "password",
            "password2",
            "first_name",
            "last_name",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        # Validate passwords match
        if data.get("password") != data.pop("password2", None):
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("Username is required")

        if CustomUser.objects.filter(username=value).exists():
            suggestions = self.generate_username_suggestions(
                self.initial_data.get("first_name", ""),
                self.initial_data.get("last_name", ""),
            )
            raise serializers.ValidationError(
                f"This username is already taken. Available suggestions: {', '.join(suggestions)}"
            )
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # Add custom claims
        data["user_id"] = self.user.id
        data["email"] = self.user.username
        return data


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission

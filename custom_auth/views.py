import time
from random import randint

from django.db.models import Q
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
)


from custom_auth.serializers import (
    UserSerializer,
    UserRegisterSerializer,
    CustomTokenObtainPairSerializer,
)
from custom_auth.tasks import (
    send_otp_email,
    send_welcome_email,
    send_reset_password_otp,
    send_success_email,
)
from custom_auth.models import CustomUser


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):

        try:
            queryset = self.get_queryset()
            user = queryset.first()

            serializer = self.get_serializer(user)

            return Response({"data": serializer.data})
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=400,
            )


class UserRegisterViewSet(viewsets.ModelViewSet):
    serializer_class = UserRegisterSerializer
    queryset = CustomUser.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Create user but set is_active to False
        user = serializer.save(is_active=False)

        # Generate OTP
        otp = str(randint(100000, 999999))

        # Store OTP in cache with 1-minute expiration
        cache_key = f"otp_{user.id}"
        cache.set(cache_key, otp, timeout=180)  # 60 seconds = 1 minute

        # Send OTP email asynchronously
        send_otp_email.delay(user.email, otp, user.first_name, user.last_name)

        return Response(
            {
                "message": "Registration successful. Please check your email for OTP verification.",
                "username": user.email,
            },
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"])
    def verify_otp(self, request):
        user_id = request.data.get("username")
        submitted_otp = request.data.get("otp")

        if not user_id or not submitted_otp:
            return Response(
                {"error": "Both user_id and otp are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(username=user_id)
            user_id = user.id
            cache_key = f"otp_{user_id}"
            stored_otp = cache.get(cache_key)

            if not stored_otp:
                return Response(
                    {
                        "error": "OTP has expired. Please request a new OTP.",
                        "can_request_new_otp": True,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if submitted_otp == stored_otp:
                user.is_active = True
                user.save()
                cache.delete(cache_key)  # Clear the OTP from cache
                send_welcome_email.delay(user.email, user.first_name, user.last_name)
                return Response({"message": "Email verified successfully"})
            else:
                return Response(
                    {"error": "Invalid OTP"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["post"])
    def resend_otp(self, request):
        username = request.data.get("username")

        if not username:
            return Response(
                {"error": "username is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(username=username)
            user_id = user.id
            cache_key = f"otp_{user_id}"

            # Check if previous OTP has expired (after 3 minutes)
            last_otp_timestamp = cache.get(f"last_otp_timestamp_{user_id}")
            current_time = time.time()

            if (
                last_otp_timestamp and current_time - last_otp_timestamp < 180
            ):  # 3 minutes
                return Response(
                    {"error": "Please wait before requesting a new OTP"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Generate and store new OTP
            new_otp = str(randint(100000, 999999))
            cache.set(cache_key, new_otp, timeout=60)  # 1 minute expiration
            cache.set(
                f"last_otp_timestamp_{user_id}", current_time, timeout=180
            )  # 3 minutes

            # Send new OTP
            send_otp_email.delay(user.email, new_otp, user.first_name, user.last_name)

            return Response({"message": "New OTP has been sent to your email"})

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["post"])
    def forgot_password(self, request):
        username = request.data.get("username")

        if not username:
            return Response(
                {"error": "username is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = CustomUser.objects.get(username=username)
            user_id = user.id
            cache_key = f"forgot_password_{user_id}"

            last_otp_timestamp = cache.get(f"last_otp_timestamp_{user_id}")
            current_time = time.time()

            if (
                last_otp_timestamp and current_time - last_otp_timestamp < 60
            ):  # 3 minutes
                return Response(
                    {"error": "Please wait before requesting a new OTP"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            new_otp = str(randint(100000, 999999))
            cache.set(cache_key, new_otp, timeout=60)
            cache.set(
                f"last_otp_timestamp_{user_id}", current_time, timeout=180
            )  # 3 minutes

            # Send new OTP
            send_reset_password_otp.delay(
                user.email, new_otp, user.first_name, user.last_name
            )

            return Response({"message": "New OTP has been sent to your email"})

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    @action(detail=False, methods=["post"])
    def reset_password(self, request):
        username = request.data.get("username")
        submitted_otp = request.data.get("otp")
        new_password = request.data.get("password")
        new_password_confirm = request.data.get("confirm_password")

        if not (username and submitted_otp and new_password and new_password_confirm):
            return Response(
                {
                    "error": "username, otp, passwords and  confirm passwords are required"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if new_password != new_password_confirm:
            return Response(
                {"error": "Passwords do not match"},
                status=status.HTTP_400_NOT_ACCEPTABLE,
            )

        try:
            user = CustomUser.objects.get(username=username)
            user_id = user.id
            cache_key = f"forgot_password_{user_id}"
            stored_otp = cache.get(cache_key)

            if not stored_otp:
                return Response(
                    {
                        "error": "OTP has expired. Please request a new OTP.",
                        "can_request_new_otp": True,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if submitted_otp == stored_otp:
                user.set_password(new_password)
                user.save()
                cache.delete(cache_key)  # Clear the OTP from cache
                send_success_email.delay(user.email, user.first_name, user.last_name)
                return Response({"message": "Password reset successfully"})
            else:
                return Response(
                    {"error": "Invalid OTP"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            return Response(
                {
                    "access": response.data["access"],
                    "refresh": response.data["refresh"],
                }
            )
        return response


class CustomTokenRefreshView(TokenRefreshView):
    serializer_class = TokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == status.HTTP_200_OK:
                return Response(
                    {
                        "access": response.data["access"],
                    }
                )
            return response
        except Exception as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

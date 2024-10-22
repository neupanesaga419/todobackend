from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from custom_auth.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):

    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    def list(self, request, *args, **kwargs):
        # Get the single user from the filtered queryset
        try:
            queryset = self.get_queryset()
            user = queryset.first()

            # Serialize the user data
            serializer = self.get_serializer(user)

            # Return the user data in the desired format
            return Response(
                {"data": serializer.data}  # Output user data directly as a dictionary
            )
        except Exception as e:
            return Response(
                {"error": str(e)},  # Output the error message as a string
                status=400,  # Set the status code to 400 (Bad Request)
            )

from django.contrib.auth.models import Permission
from custom_auth.models import CustomUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView, Response


class PermissionViewSet(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_permissions = CustomUser.objects.get(
            email=request.user.email
        ).get_all_permissions()

        return Response({"permissions": list(user_permissions)})

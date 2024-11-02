from django.urls import path
from rest_framework.routers import DefaultRouter
from custom_auth.views import (
    UserViewSet,
    UserRegisterViewSet,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
)


router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("register", UserRegisterViewSet, basename="register")


urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls

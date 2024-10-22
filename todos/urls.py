from django.urls import path
from rest_framework.routers import DefaultRouter

from todos.views import TodoViewSet

router = DefaultRouter()
router.register(r"todos", TodoViewSet)

urlpatterns = router.urls

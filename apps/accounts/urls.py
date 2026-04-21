from rest_framework.routers import DefaultRouter
from .views import UserAdminViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('users', UserAdminViewSet, basename='administrator')

urlpatterns = [
    path('admin/', include(router.urls)),
]
    
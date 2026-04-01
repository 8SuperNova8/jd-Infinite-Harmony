from rest_framework import routers
from django.urls import path, include
from apps.payments.views import PaymentAdminViewSet

router = routers.DefaultRouter()
router.register('payments', PaymentAdminViewSet)

urlpatterns = [
    path('admin/', include(router.urls))
]
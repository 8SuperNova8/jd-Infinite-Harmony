from rest_framework import routers
from django.urls import path, include
from apps.payments.views import PaymentViewSets

router = routers.DefaultRouter()
router.register('payments', PaymentViewSets)

urlpatterns = [
    path('', include(router.urls))
]
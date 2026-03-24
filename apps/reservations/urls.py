from rest_framework import routers
from apps.reservations.views import ReservationViewSets
from django.urls import path, include

router = routers.DefaultRouter()
router.register ('reservations', ReservationViewSets)

urlpatterns = [
    path('', include(router.urls)),
]
from rest_framework import routers
from django.urls import path, include
from . import views

router = routers.DefaultRouter()
router.register ('rooms', views.RoomViewSets)
router.register (r'room-types', views.RoomTypeViewSets)

urlpatterns = [
    path('', include(router.urls)),
]
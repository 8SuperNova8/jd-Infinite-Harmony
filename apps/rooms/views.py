from rest_framework import viewsets, status, mixins
from datetime import datetime
from apps.rooms.models import Room, RoomType
from apps.rooms.serializers import RoomSerializer, RoomTypeSerializer
from .mixins import AvailableRoomsMixin
from rest_framework.permissions import IsAdminUser, AllowAny

#Perfil Publico
class RoomTypeViewSet (
    mixins.ListModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = RoomTypeSerializer
    queryset = RoomType.objects.all()
    permission_classes = [AllowAny]

class RoomViewSet (
    viewsets.GenericViewSet,
    AvailableRoomsMixin
    ):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [AllowAny]

#***************************

#permisos para Admin
class RoomTypeAdminViewset (viewsets.ModelViewSet):
    serializer_class= RoomTypeSerializer
    queryset = RoomType.objects.all()
    permission_classes = [IsAdminUser]

    
class RoomAdminViewSet(
    viewsets.ModelViewSet,
    AvailableRoomsMixin
    ):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = [IsAdminUser]
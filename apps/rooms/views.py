from rest_framework import viewsets, status
from apps.rooms.models import Room, RoomType
from apps.rooms.serializers import RoomSerializer, RoomTypeSerializer, AvailableRoomSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, OuterRef, Exists, Case, When, Value, CharField
from datetime import datetime
from apps.reservations.models import Reservation


class RoomTypeViewSets (viewsets.ModelViewSet):
    serializer_class = RoomTypeSerializer
    queryset = RoomType.objects.all()

class RoomViewSets (viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()

    @action(detail=False, methods=['get'])
    def available(self, request):
        serialicer = AvailableRoomSerializer(data=request.query_params)
        serialicer.is_valid(raise_exception=True)
        data = serialicer.validated_data

        #trae todos los Id de habitaciones que solapan con fechas 
        overlapping_dates = Reservation.objects.filter(
            room = OuterRef('pk'),
            check_in__lt = data['check_out'],
            check_out__gt = data['check_in'],
            status__in =[ 'confirmed', 'checked_in'] # __in es un lookup de Django que sirve para buscar valores dentro de una lista
        )

        #todas las habitaciones disponibles por tipo de habitacion 
        rooms = Room.objects.filter(
            room_type_id = data['room_type'],
        ).annotate(
            is_occupied = Exists(overlapping_dates)
        ).annotate(
            availability = Case(
                When(is_occupied = True, then=Value('occupied')),
                When(status = 'maintenance', then=Value('occupied')),
                When(status = 'inactive', then=Value('occupied')),
                default = Value('available'),
                output_field = CharField()
            )
        )

        return Response(rooms.values(
            'id',
            'room_number',
            'floor',
            'availability'
        ))

        

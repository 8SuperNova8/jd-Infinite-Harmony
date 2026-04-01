from datetime import date
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ReservationFilter
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from apps.reservations.models import Reservation
from apps.reservations.serializers import ReservationSerializer, ChangeStatusSerializer
from django.db import transaction
from .throttles import ReservationThrottle


class ReservationViewSet (#para publico
    mixins.CreateModelMixin, #solo crear
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [AllowAny]
    
    #valida por token
    lookup_field = 'token' #modifica el endpoint de consulta de pk por token
    lookup_url_kwarg = 'token'#dice “el parámetro en la URL se llama token”
    lookup_value_regex = '[0-9a-f-]{36}' # solo permite formato UUID

    #aplica el limite de peticion de solo reserva esto esta en settings
    throttle_classes = [ReservationThrottle] 

    #no permite duplicados db
    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    # --- ENDPOINTS PARA CANCELAR 
    #para publico 
    @action(detail=True, methods=['patch'])
    def cancel(self, request, token=None):
        reservation = self.get_object()

        if reservation.status != 'confirmed':
            return Response({'Error': 'Solo reservas confirmadas se pueden cancelar'}, status=status.HTTP_400_BAD_REQUEST)


        reservation.status = 'cancelled'
        reservation.save()
        return Response ({'status' : 'cancelled'}, status=status.HTTP_200_OK)
        
# ------------ ADMIN -----------------       

class AdminReservationViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    permission_classes = [IsAdminUser]

    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter

    

    # para Admin
    # confirmed ->chek_in o -> no_show
    @action(detail=True, methods=['patch'])
    def change_status (self, request, pk=None):
        reservation = self.get_object()
        #new_status = request.data.get('status')
        serializer = ChangeStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_status = serializer.validated_data['status']

        if not serializer.is_valid():
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

        allowed = {
            'confirmed' :['checked_in', 'no_show', 'cancelled'],
            'checked_in' :['finished']
        }

        if not new_status or new_status not in allowed.get(reservation.status, []) :
            return Response({'error': 'invalido el cambio'}, status=status.HTTP_400_BAD_REQUEST)
        
        reservation.status = new_status
        reservation.save()

        return Response({
            'id':reservation.id,
            'status': reservation.status
        }, status=status.HTTP_200_OK)

'''
    
    #configuracion de los filtros 
    def get_queryset(self):
        queryset = Reservation.objects.all()
        params = self.request.query_params

        #filtro por estado
        status_param = params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)

        #filtro por habitación
        room = params.get('room_id')
        if room:
            queryset = queryset.filter(room_id=room)

        #filtro por document
        document = params.get('guest_document')
        if document:
            queryset = queryset.filter(guest_document=document)

        #filtro por rango de fechas
        check_in= params.get('check_in')
        check_out = params.get('check_out')
        if check_in and check_out:
            queryset = queryset.filter(
                check_in__lt=check_out,
                check_out__gt=check_in
                )
        #filtro por fecha especifica
        date= params.get('date')
        if date:
            queryset =  queryset.filter(
                check_in__lte = date,
                check_out__gt =date
            )

        return queryset
    

______________________________________
    
    #valido la informacion desde el serializer esto era para document
    def list(self, request, *args, **kwargs):
        get_document = ReservationQueryGetCCSerializer(data=request.query_params)
        get_document.is_valid(raise_exception=True)
        return super().list(request, *args, **kwargs) # esto manda a ejecutar Get_queryset

    def get_queryset(self):
        document = self.request.query_params.get('document')

        queryset = self.queryset.filter(guest_document = document).order_by('-reservation_date')
        return queryset #retorna un queryset con todos las reservas 
        
    '''
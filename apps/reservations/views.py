from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.reservations.models import Reservation
from apps.reservations.serializers import ReservationSerializer
from django.db import transaction
from .throttles import ReservationThrottle


class ReservationViewSets (#para publico
    mixins.CreateModelMixin, #solo crear
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ReservationSerializer
    queryset = Reservation.objects.all()
    
    #valida por token
    lookup_field = 'token' #modifica el endpoint de consulta de pk por token
    lookup_value_regex = '[0-9a-f-]{36}' # solo permite formato UUID

    #aplica el limite de peticion de solo reserva esto esta en settings
    throttle_classes = [ReservationThrottle] 

    #no permite duplicados db
    @transaction.atomic
    def perform_create(self, serializer):
        serializer.save()

    # --- ENDPOINTS PARA CANCELAR 
    #para publico 
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        token = request.query_params.get('token')

        if not token or reservation.token != token:
            return Response({'error': 'Token no valido'}, staus=status.HTTP_403_FORBIDDEN)

        if reservation.status != 'confirmed':
            return Response({'Error': 'Solo reservas confirmadas se pueden cancelar'}, status=status.HTTP_400_BAD_REQUEST)


        reservation.status = 'cancelled'
        reservation.save()
        return Response ({'status' : 'cancelled'}, status=status.HTTP_200_OK)
        


    # para Admin
    # confirmed ->chek_in o -> no_show
    @action(detail=True, methods=['post'])
    def change_status (self, request, pk=None):
        reservation = self.get_object()
        new_status = request.data.get('status')

        allowed = {
            'confirmed' :['checked_in', 'no_show', 'cancelled'],
            'checked_in' :['finished']
        }

        if new_status not in allowed.get(reservation.status, [] or not new_status):
            return Response({'error': 'invalido el cambio'}, status=status.HTTP_400_BAD_REQUEST)
        
        reservation.status = new_status
        reservation.save()

        return Response({
            'id':reservation.id,
            'status': reservation.status
        }, status=status.HTTP_200_OK)


    '''
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
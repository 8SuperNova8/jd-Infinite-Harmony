from rest_framework import serializers
from apps.reservations.models import Reservation
from .services.reservation_value import reservation_value

#creacion de reserva para admin y public
class ReservationSerializer (serializers.ModelSerializer):
    guest_email = serializers.EmailField()
    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True)

    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out', 'guest_name', 'guest_email', 'guest_phone', 'guest_document', 'room', 'total_amount' ]

    def create(self, validated_data):
        room = validated_data['room']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']

        validated_data['total_amount'] = reservation_value(room, check_in, check_out)

        return super().create(validated_data)
    
    #valida si existe reserva 
    def validate (self, data):
        check_in= data['check_in']
        check_out = data['check_out']
        #valida que fecha de salida no sea menor que entrada
        if check_out <= check_in:
            raise serializers.ValidationError('Check-out must be after check-in')

        #verifica si la habitacion tiene alguna reserva para esa fecha 
        overlapping = Reservation.objects.filter(
            room = data['room'],
            check_in__lt= data['check_out'],
            check_out__gt = data['check_in'],
            status__in = ['confirmed', 'checked_in']
        ).exists() #esto devuelve un booleano

        if overlapping:
            raise serializers.ValidationError(
                'This room is already reserved for those dates.'
            )
        return data
    
#detalle para public 
class ReservationPublicDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['check_in', 'check_out', 'reservation_date', 'status', 'guest_name', 'total_amount']

#detalle para Admin
class ReservationAdminSerializer(serializers.ModelSerializer):
    total_real = serializers.ReadOnlyField()
    total_paid = serializers.ReadOnlyField()
    balance = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = "__all__"
  

class ChangeStatusSerializer(serializers.Serializer):
    status = serializers.CharField()

    def validate(self, data):
        #verificar campos adicioales
        alowed_fields = {'status'}
        received_fields = set(self.initial_data.keys())

        if received_fields != alowed_fields:
            raise serializers.ValidationError('Only the "status" field can be modified')
        return data
    
class ExtraChargesSerializer(serializers.Serializer):
    extra_charges = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0
    )

'''
class AddExtraChargesSerializer(serializers.Serializer):
    extra_charges= serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )

'''
    
'''    
#consulta por cedula 
class ReservationQueryGetCCSerializer (serializers.Serializer):
    token = serializers.models.UUIDField(
        default=uuid.uuid4, 
        editable=False,
        unique=True
    )
        
    def validate_token(self, value):
        if not value.isdigit():
            raise serializers.ValidationError('Debe ser token')
        return value  
'''

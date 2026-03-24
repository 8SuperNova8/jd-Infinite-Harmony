from rest_framework import serializers
from apps.reservations.models import Reservation

#formulario de reserva
class ReservationSerializer (serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'

    def create(self, validated_data):
        room = validated_data['room']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']

        nights = (check_out- check_in).days
        price = room.room_type.base_price
        total = nights * price

        validated_data['total_amount'] = total

        return super().create(validated_data)
    
    #valida si existe reserva 
    def validate (self, data):

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

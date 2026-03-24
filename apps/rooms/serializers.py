from rest_framework import serializers
from apps.rooms.models import Room, RoomType

class RoomTypeSerializer (serializers.ModelSerializer):
    class Meta:
        model = RoomType
        fields = '__all__'

class RoomSerializer (serializers.ModelSerializer):
    #room_type = RoomTypeSerializer(read_only=True)
    class Meta:
        model = Room
        fields = '__all__'

#verifica data de la busqueda de disponibilidad
class AvailableRoomSerializer (serializers.Serializer):
    room_type = serializers.IntegerField()
    check_in = serializers.DateField(input_formats=['%Y-%m-%d'])    
    check_out = serializers.DateField(input_formats=['%Y-%m-%d'])

    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError(
                'check_in debe ser menor que check_out'
            )
        return data
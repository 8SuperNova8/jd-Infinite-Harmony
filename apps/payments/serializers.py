from rest_framework import serializers
from apps.payments.models import Payment
from .services.payment_service import create_payment

class PaymentSerializer (serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('payment_date',)
        

    def create(self, validated_data):
        reservation = validated_data['reservation']
        amount = validated_data['amount']
        payment_method = validated_data['payment_method']
        status = validated_data.get('status', 'completed')

        return create_payment(
            reservation=reservation,
            amount=amount,
            payment_method=payment_method,
            status=status
        )
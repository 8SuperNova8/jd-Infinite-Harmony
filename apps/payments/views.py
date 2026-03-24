from rest_framework import viewsets
from apps.payments.serializers import PaymentSerializer
from apps.payments.models import Payment

class PaymentViewSets (viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

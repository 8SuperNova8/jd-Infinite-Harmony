from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAdminUser
from apps.payments.serializers import PaymentSerializer
from apps.payments.models import Payment

class PaymentAdminViewSet (
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
    ):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAdminUser]

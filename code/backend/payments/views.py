from rest_framework import viewsets

from . import models as m
from . import serializers as s


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = m.Payment.objects.all()
    serializer_class = s.PaymentSerializer


class SimplePayTransactionViewSet(viewsets.ModelViewSet):
    queryset = m.SimplePayTransaction.objects.all()
    serializer_class = s.SimplePayTransactionSerializer

from rest_framework import viewsets

from . import models as m
from . import serializer as s


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = m.Payment.objects.all()
    serializer_class = s.PaymentSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = m.Transaction.objects.all()
    serializer_class = s.TransactionSerializer

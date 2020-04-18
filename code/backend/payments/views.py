from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from appointments.models import Appointment
from . import models as m
from . import serializers as s


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = m.Payment.objects.all()
    serializer_class = s.PaymentSerializer


class SimplePayTransactionViewSet(viewsets.ModelViewSet):
    queryset = m.SimplePayTransaction.objects.all()
    serializer_class = s.SimplePayTransactionSerializer


class GetPriceView(mixins.RetrieveModelMixin, generics.GenericAPIView):
    serializer_class = s.GetPriceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        res = self._calculate_price(appointment)
        return Response(res, status=status.HTTP_200_OK,)

    def _calculate_price(self, appointment):
        return {
            "total_price": 30_000,
            "currency": "HUF",
        }

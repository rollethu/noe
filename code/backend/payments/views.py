from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from appointments.models import Appointment
from .prices import calc_payments
from . import models as m
from . import serializers as s


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = m.Payment.objects.all()
    serializer_class = s.PaymentSerializer


class SimplePayTransactionViewSet(viewsets.ModelViewSet):
    queryset = m.SimplePayTransaction.objects.all()
    serializer_class = s.SimplePayTransactionSerializer


class _PaymentMixin:
    def _get_appointment(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment = serializer.save()
        payment_method_type = serializer.validated_data["payment_method_type"]
        return appointment, payment_method_type


class GetPriceView(_PaymentMixin, generics.GenericAPIView):
    serializer_class = s.GetPriceSerializer

    def post(self, request, *args, **kwargs):
        appointment, payment_method_type = self._get_appointment(request)
        _, summary = calc_payments(appointment.seats.all(), payment_method_type)
        return Response(summary, status=status.HTTP_200_OK,)


class PayView(_PaymentMixin, generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        appointment, payment_method_type = self._get_appointment(request)
        payments, summary = calc_payments(appointment.seats.all(), payment_method_type)
        # TODO: validate payment amount
        m.Payment.objects.bulk_create(payments)
        appointment.is_registration_completed = True
        appointment.save()
        return Response(summary, status=status.HTTP_200_OK,)

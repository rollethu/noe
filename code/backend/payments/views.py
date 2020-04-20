from urllib.parse import urlparse
from django.urls import resolve
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from appointments.models import Appointment
from .prices import calc_payments
from . import models as m
from . import serializers as s


class _PaymentMixin:
    def _get_appointment(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment_uuid = self._get_appointment_uuid(serializer.validated_data["appointment"])
        appointment = Appointment.objects.get(pk=appointment_uuid)
        return appointment, serializer.validated_data

    def _get_appointment_uuid(self, appointment_url):
        parsed_url = urlparse(appointment_url)
        match = resolve(parsed_url.path)
        appointment_uuid = match.kwargs["pk"]
        return appointment_uuid


class GetPriceView(_PaymentMixin, generics.GenericAPIView):
    """Query the price of the Appointment.
    Get the Appointment ID in POST request body, so we don't leak it accidentally.
    """

    serializer_class = s.GetPriceSerializer

    def post(self, request, *args, **kwargs):
        appointment, validated_data = self._get_appointment(request)
        # This is a public endpoint. Make sure someone can't brute force find prices for finished registrations.
        if appointment.is_registration_completed:
            raise ValidationError({"appointment": "This appointment registration has already been closed."})
        _, summary = calc_payments(appointment.seats.all(), validated_data["payment_method_type"])
        return Response(summary, status=status.HTTP_200_OK)


class PayAppointmentView(_PaymentMixin, generics.GenericAPIView):
    """Called at the end of registration when user presses the Pay button."""

    serializer_class = s.PaySerializer

    def post(self, request, *args, **kwargs):
        appointment, validated_data = self._get_appointment(request)

        if appointment.is_registration_completed:
            raise ValidationError({"appointment": "This appointment registration has already been closed."})
        if appointment.seats.count() == 0:
            raise ValidationError({"appointment": "This appointment has no persons yet!"})

        payments, summary = calc_payments(appointment.seats.all(), validated_data["payment_method_type"])

        # This is just a sanity check, so we don't calculate a wrong amount.
        # What we show on the frontend, should always match on the backend.
        if summary["total_price"] != validated_data["total_price"]:
            raise ValidationError({"total_price": "Invalid amount!"})

        m.Payment.objects.bulk_create(payments)
        return Response(summary, status=status.HTTP_200_OK)

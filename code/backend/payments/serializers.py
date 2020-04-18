from urllib.parse import urlparse
from django.urls import resolve
from rest_framework import serializers
from appointments.models import Appointment
from . import models as m


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Payment
        fields = "__all__"


class SimplePayTransactionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.SimplePayTransaction
        fields = "__all__"


class _GetAppointmentMixin:
    def create(self, validated_data):
        parsed_url = urlparse(validated_data["appointment"])
        match = resolve(parsed_url.path)
        appointment_uuid = match.kwargs["pk"]
        return Appointment.objects.get(pk=appointment_uuid)


class GetPriceSerializer(_GetAppointmentMixin, serializers.HyperlinkedModelSerializer):
    appointment = serializers.URLField(write_only=True)
    payment_method_type = serializers.CharField(write_only=True)

    total_price = serializers.FloatField(read_only=True)
    currency = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ["appointment", "payment_method_type", "total_price", "currency"]


class PaySerializer(_GetAppointmentMixin, serializers.HyperlinkedModelSerializer):
    appointment = serializers.URLField()
    payment_method_type = serializers.CharField()
    total_price = serializers.FloatField()

    currency = serializers.CharField(read_only=True)

    class Meta:
        model = Appointment
        fields = ["appointment", "payment_method_type", "total_price", "currency"]

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from appointments.models import Appointment
from .prices import PRODUCT_CHOICES, PRODUCTS
from . import models as m


class PaySerializer(serializers.Serializer):
    appointment = serializers.HyperlinkedRelatedField(
        view_name="appointment-detail", queryset=Appointment.objects.all(), write_only=True
    )
    product_type = serializers.ChoiceField(choices=PRODUCT_CHOICES)

    total_price = serializers.FloatField()
    currency = serializers.CharField()

    class Meta:
        fields = ["appointment", "product_type", "total_price", "currency"]

    def create(self, validated_data):
        if validated_data["appointment"].is_registration_completed:
            raise ValidationError({"appointment": "This appointment registration has already been closed."})
        product = PRODUCTS[validated_data["product_type"]]
        return validated_data["appointment"], product


class GetPriceSerializer(PaySerializer):
    total_price = serializers.FloatField(read_only=True)
    currency = serializers.CharField(read_only=True)

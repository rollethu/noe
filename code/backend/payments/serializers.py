from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from appointments.models import Appointment
from feature_flags import use_feature_simplepay
from .prices import PRODUCT_CHOICES, PRODUCTS, PAYMENT_METHOD_TYPE_CHOICES
from . import models as m


class _BasePaySerializer(serializers.Serializer):
    appointment = serializers.HyperlinkedRelatedField(
        view_name="appointment-detail", queryset=Appointment.objects.all(), write_only=True
    )
    product_type = serializers.ChoiceField(choices=PRODUCT_CHOICES)

    def create(self, validated_data):
        if validated_data["appointment"].is_registration_completed:
            raise ValidationError({"appointment": "This appointment registration has already been closed."})
        product = PRODUCTS[validated_data["product_type"]]
        return validated_data["appointment"], product


class GetPriceSerializer(_BasePaySerializer):
    total_price = serializers.DecimalField(read_only=True, max_digits=7, decimal_places=2)
    currency = serializers.CharField(read_only=True)

    class Meta:
        fields = ["appointment", "product_type", "total_price", "currency"]


class PaySerializer(_BasePaySerializer):
    total_price = serializers.DecimalField(max_digits=7, decimal_places=2)
    currency = serializers.CharField()
    payment_method = serializers.ChoiceField(choices=PAYMENT_METHOD_TYPE_CHOICES, required=use_feature_simplepay)

    class Meta:
        fields = ["appointment", "product_type", "total_price", "currency", "payment_method"]

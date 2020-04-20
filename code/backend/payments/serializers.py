from rest_framework import serializers
from .prices import PAYMENT_METHOD_TYPE_CHOICES
from . import models as m


class GetPriceSerializer(serializers.Serializer):
    appointment = serializers.URLField(write_only=True)
    payment_method_type = serializers.ChoiceField(choices=PAYMENT_METHOD_TYPE_CHOICES)

    total_price = serializers.FloatField(read_only=True)
    currency = serializers.CharField(read_only=True)

    class Meta:
        fields = ["appointment", "payment_method_type", "total_price", "currency"]


class PaySerializer(serializers.Serializer):
    appointment = serializers.URLField()
    payment_method_type = serializers.ChoiceField(choices=PAYMENT_METHOD_TYPE_CHOICES)
    total_price = serializers.FloatField()
    currency = serializers.CharField()

    class Meta:
        fields = ["appointment", "payment_method_type", "total_price", "currency"]

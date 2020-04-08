from rest_framework import serializers

from . import models as m


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Payment
        fields = "__all__"

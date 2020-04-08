from rest_framework import serializers

from . import models as m


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Sample
        fields = "__all__"


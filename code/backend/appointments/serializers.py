from rest_framework import serializers

from . import models as m


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Location
        fields = "__all__"


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    location_name = serializers.CharField(source="location.name", default="", read_only=True)

    class Meta:
        model = m.Appointment
        fields = "__all__"
        extra_kwargs = {
            "location": {"allow_null": False},
            "licence_plate": {"allow_blank": False},
        }


class SeatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Seat
        fields = "__all__"

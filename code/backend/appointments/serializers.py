from rest_framework import serializers

from . import models as m


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Location
        fields = "__all__"


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Appointment
        fields = [
            "url",
            "email",
            "gtc",
            "privacy_policy",
            "start",
            "end",
            "phone_number",
            "licence_plate",
            "normalized_licence_plate",
            # FIXME: avoid n+1, this is currently referencing location.name
            "location_name",
            "location",
        ]
        extra_kwargs = {
            "location": {"allow_null": False},
            "licence_plate": {"allow_blank": False},
        }


class SeatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Seat
        fields = "__all__"

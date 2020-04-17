from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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


class VerifyEmailSerializer(serializers.Serializer):
    appointment_url = serializers.HyperlinkedIdentityField(read_only=True, view_name="appointment-detail")
    appointment_email = serializers.EmailField(read_only=True, source="email")
    token = serializers.CharField(write_only=True, max_length=255)

    def create(self, validated_data):
        try:
            ev, signed_uuid = m.EmailVerification.objects.get_by_token(validated_data["token"])
            ev.verify(signed_uuid)
        except Exception:
            raise ValidationError({"token": "Invalid token"})

        return ev.appointment

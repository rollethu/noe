from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models as m


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Location
        fields = "__all__"


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    location_name = serializers.CharField(source="location.name", default="", read_only=True)
    email_verification_uuid = serializers.SerializerMethodField()

    def get_email_verification_uuid(self, obj):
        ev = obj.email_verifications.first()
        return ev.uuid if ev else None

    class Meta:
        model = m.Appointment
        fields = "__all__"
        extra_kwargs = {
            "location": {"allow_null": False},
            "licence_plate": {"allow_blank": False},
        }

    def update(self, instance, validated_data):
        self._bump_time_slot_usage(instance, validated_data)
        appointment = super().update(instance, validated_data)

        return appointment

    def _bump_time_slot_usage(self, appointment, validated_data):
        time_slot = validated_data.get("time_slot")
        if not time_slot:
            return

        seat_count = appointment.seats.count()
        # TODO: Uncomment if we want to forbid overbooking
        # if time_slot.capacity - time_slot.usage < seat_count:
        #     raise ValidationError({"time_slot": "Idősáv már tele. Válasszon másik idősávot."})

        time_slot.usage += seat_count
        time_slot.save()


class SeatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Seat
        fields = "__all__"

    def create(self, validated_data):
        self._validate_healthcare_number_with_referral(validated_data)
        return super().create(validated_data)

    def _validate_healthcare_number_with_referral(self, validated_data):
        has_doctor_referral = validated_data.get("has_doctor_referral")
        healthcare_number = validated_data.get("healthcare_number")
        if has_doctor_referral and not healthcare_number:
            raise ValidationError({"healthcare_number": _("This field is required.")})


class VerifyEmailSerializer(serializers.Serializer):
    appointment_url = serializers.HyperlinkedIdentityField(read_only=True, view_name="appointment-detail")
    appointment_email = serializers.EmailField(read_only=True, source="email")
    token = serializers.CharField(write_only=True, max_length=255)

    def create(self, validated_data):
        try:
            ev, signed_uuid = m.EmailVerification.objects.get_by_token(validated_data["token"])
            ev.verify(signed_uuid)
        except ValueError as e:
            raise ValidationError({"token": str(e)})
        except Exception:
            raise ValidationError({"token": "Invalid token"})

        return ev.appointment


class ResendEmailVerificationSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = m.EmailVerification
        fields = ["uuid"]


class TimeSlotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.TimeSlot
        fields = "__all__"

from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from . import models as m
from . import licence_plates
from . import phone_numbers
from . import utils as u


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        ref_name = "Public Location"
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
        ref_name = "Public Appointments"
        extra_kwargs = {
            "location": {"allow_null": False},
            "licence_plate": {"allow_blank": False},
            "time_slot": {"allow_null": False},
        }

    def update(self, instance, validated_data):
        self._bump_time_slot_usage(instance, validated_data)
        self._validate_location_change(instance, validated_data)

        # Licence plate should only be added as an update,
        # but not during creation
        licence_plate = validated_data.get("licence_plate", None)
        if licence_plate is not None:
            validated_data["normalized_licence_plate"] = licence_plates.get_normalized_licence_plate(licence_plate)

        appointment = super().update(instance, validated_data)
        self._match_appointment_start_and_end_with_time_slot(appointment)
        return appointment

    def _bump_time_slot_usage(self, appointment, validated_data):
        time_slot = validated_data.get("time_slot")
        if not time_slot:
            return

        if time_slot.start <= timezone.now():
            raise ValidationError({"time_slot": _("You can not choose time slots started in the past")})

        availability = time_slot.capacity - time_slot.usage
        required_space = appointment.seats.count()
        if availability < required_space:
            raise ValidationError({"time_slot": _("Time slot doesn't have enough capacity")})

        seat_count = appointment.seats.count()

        time_slot.add_usage(seat_count)
        time_slot.save()

    def _match_appointment_start_and_end_with_time_slot(self, appointment):
        start, end = None, None
        if appointment.time_slot is not None:
            start = appointment.time_slot.start
            end = appointment.time_slot.end

        appointment.start = start
        appointment.end = end
        appointment.save()

    def _validate_location_change(self, appointment, validated_data):
        current_location = appointment.location
        if current_location and validated_data["location"] != current_location:
            raise ValidationError({"location": _("Location can not be replaced")})


class SeatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.Seat
        exclude = ["has_doctor_referral"]
        ref_name = "Public Seat"

    def create(self, validated_data):
        self._validate_healthcare_number_with_referral(validated_data)
        return super().create(validated_data)

    def validate_healthcare_number(self, data):
        if data and not u.is_healthcare_number_valid(data):
            raise ValidationError(_("Invalid format"))
        return data

    def validate_appointment(self, appointment):
        if appointment.seats.count() >= m.MAX_SEATS_PER_APPOINTMENT:
            raise ValidationError(
                _("Maximum %(max_seat_count)s Seats can belong to an appointment")
                % {"max_seat_count": m.MAX_SEATS_PER_APPOINTMENT}
            )
        return appointment

    def validate_birth_date(self, birth_date):
        if birth_date > timezone.now().date():
            raise ValidationError(_("Birth date must be in the past."))
        return birth_date

    def validate_phone_number(self, raw_phone_number):
        try:
            return phone_numbers.get_normalized_phone_number(raw_phone_number, check_validity=True)
        except phone_numbers.InvalidPhoneNumber:
            raise ValidationError(_("Invalid phone number."))

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
        fields = ["url", "start", "end"]
        ref_name = "Public TimeSlot"

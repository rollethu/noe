from django.db import transaction
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from payments import services as payment_services
from appointments.models import Location, Appointment, Seat
from payments.models import Payment
from samples.models import Sample


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="staff-payment-detail")

    class Meta:
        model = Payment
        ref_name = "Staff Payment"
        fields = ["url", "amount", "currency", "paid_at", "product_type", "payment_method_type", "proof_number"]
        read_only_fields = ["amount", "currency", "product_type"]

    @transaction.atomic
    def update(self, instance, validated_data):
        original_paid_at = instance.paid_at
        try:
            payment_services.validate_paid_at(original_paid_at, validated_data)
        except ValueError as e:
            raise ValidationError({"paid_at": e})

        rv = super().update(instance, validated_data)
        payment_services.handle_paid_at(original_paid_at, instance.seat, validated_data)
        return rv


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="staff-appointment-detail")
    all_seats_paid = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        ref_name = "Staff Appointment"
        fields = [
            "url",
            "location",
            "start",
            "end",
            "all_seats_paid",
            "normalized_licence_plate",
            "is_registration_completed",
        ]

    def get_all_seats_paid(self, obj):
        # This works, because Payment.DoesNotExist is also an AttributeError
        has_payment = lambda s: getattr(s, "payment", None) is not None
        seat_qs = obj.seats.all()
        return all(has_payment(s) and s.payment.is_paid for s in seat_qs)


class SeatSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="staff-seat-detail")
    appointment = AppointmentSerializer(read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Seat
        ref_name = "Staff Seat"
        fields = [
            "url",
            "full_name",
            "birth_date",
            "identity_card_number",
            "has_doctor_referral",
            "healthcare_number",
            "appointment",
            "payment",
        ]


class SampleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="staff-sample-detail")
    seat = serializers.HyperlinkedRelatedField(view_name="staff-seat-detail", queryset=Seat.objects.all())
    location = serializers.HyperlinkedRelatedField(view_name="location-detail", queryset=Location.objects.all())
    status = serializers.ChoiceField(choices=Sample.SAMPLE_STATUS_CHOICES, required=True)

    class Meta:
        model = Sample
        fields = ["url", "seat", "location", "vial", "status", "sampled_at"]

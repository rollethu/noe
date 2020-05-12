from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from billing.services import send_invoice
from appointments.models import Location, Appointment, Seat
from payments.models import Payment
from samples.models import Sample
from feature_flags import use_feature_billing_details


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="staff-payment-detail")

    class Meta:
        model = Payment
        ref_name = "Staff Payment"
        fields = ["url", "amount", "currency", "paid_at", "product_type", "payment_method_type", "proof_number"]
        read_only_fields = ["amount", "currency", "product_type"]

    def update(self, instance, validated_data):
        if use_feature_billing_details:
            self._handle_paid_at(instance, validated_data)
        return super().update(instance, validated_data)

    def _handle_paid_at(self, payment, validated_data):
        new_paid_at = validated_data.get("paid_at", False)
        if new_paid_at is False:
            return

        if new_paid_at is not False and new_paid_at != payment.paid_at:
            raise ValidationError({"paid_at": _("Paid at can not be changed")})

        send_invoice(payment.seat)


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

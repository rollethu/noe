from rest_framework import serializers
from appointments.models import Appointment, Seat
from payments.models import Payment


class PaymentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="staff-payment-detail")

    class Meta:
        model = Payment
        fields = ["url", "amount", "currency", "paid_at", "payment_method_type"]


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="staff-appointment-detail")
    all_seats_paid = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
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
        fields = [
            "url",
            "full_name",
            "identity_card_number",
            "has_doctor_referral",
            "healthcare_number",
            "appointment",
            "payment",
        ]

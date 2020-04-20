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

    class Meta:
        model = Appointment
        fields = ["url", "location", "start", "end", "licence_plate", "is_registration_completed"]


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

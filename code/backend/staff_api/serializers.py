from rest_framework import serializers
from appointments.models import Appointment, Seat


class AppointmentSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="staff-appointment-detail")

    class Meta:
        model = Appointment
        fields = ["url", "location", "start", "end", "licence_plate"]


class SeatSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="staff-seat-detail")
    # appointment = serializers.HyperlinkedRelatedField(read_only=True, view_name="staff-appointment-detail")
    appointment = AppointmentSerializer()

    class Meta:
        model = Seat
        fields = ["url", "full_name", "identity_card_number", "appointment"]

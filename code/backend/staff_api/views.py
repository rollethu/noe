from rest_framework import viewsets
from appointments.models import Appointment, Seat
from . import serializers as s


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = s.AppointmentSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = s.SeatSerializer

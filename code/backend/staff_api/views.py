from rest_framework import routers, viewsets
from appointments.models import Appointment, Seat
from . import serializers as s


class StaffAPIRoot(routers.APIRootView):
    """
    REST API endpoints for staff members.
    """


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = s.AppointmentSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = s.SeatSerializer

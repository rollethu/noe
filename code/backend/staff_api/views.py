from django.urls import reverse as django_reverse
from django.shortcuts import redirect
from rest_framework import routers, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from appointments.models import Appointment, Seat
from payments.models import Payment
from . import serializers as s
from . import filters as f


class StaffAPIRoot(routers.APIRootView):
    """
    REST API endpoints for staff members.
    """

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)


class _StaffViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class AppointmentViewSet(_StaffViewSet):
    queryset = Appointment.objects.all()
    serializer_class = s.AppointmentSerializer
    filterset_class = f.AppointmentFilter


class SeatViewSet(_StaffViewSet):
    queryset = Seat.objects.all()
    serializer_class = s.SeatSerializer

    def retrieve(self, request, *args, **kwargs):
        if "USE-STAFF-API" not in request.headers:
            return redirect(django_reverse("admin:appointments_seat_change", kwargs={"object_id": kwargs["pk"]}))
        return super().retrieve(request)


class PaymentViewSet(_StaffViewSet):
    queryset = Payment.objects.all()
    serializer_class = s.PaymentSerializer

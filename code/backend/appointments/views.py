import os
import logging
from urllib.parse import urlencode
from django.db import transaction
from django.conf import settings
from django.contrib import messages
from django.urls import reverse as django_reverse
from django.utils import timezone
from django.utils.translation import gettext as _
from django.shortcuts import redirect, get_object_or_404
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from rest_framework import routers
from rest_framework import mixins
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.settings import api_settings
from project_noe.views import NoReadModelViewSet
from . import auth
from . import filters as f
from . import models as m
from . import serializers as s
from . import email
from . import permissions


logger = logging.getLogger(__name__)


class ApiRootView(routers.APIRootView):
    permission_classes = [IsAdminUser]


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = m.Location.objects.all()
    serializer_class = s.LocationSerializer


class AppointmentViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = m.Appointment.objects.all()
    serializer_class = s.AppointmentSerializer
    authentication_classes = [auth.AppointmentAuthentication]
    permission_classes = [permissions.AppointmentPermission]

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        return super().get_permissions()

    def has_object_permission(self, request, view, obj):
        return request.appointment == obj

    def perform_create(self, serializer):
        appointment = serializer.save()
        # FIXME: this is ugly, but works until we have only one email
        # for every appointment
        ev = appointment.email_verifications.first()
        token = ev.make_token()
        email.send_verification(token, serializer.validated_data["email"])

    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        appointment = self.get_object()
        serializer = self.get_serializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        is_registration_completed = serializer.validated_data.get("is_registration_completed", False)
        if is_registration_completed:
            self._make_qrs(appointment.seats.all())

        self.perform_update(serializer)

        if is_registration_completed:
            # we need to refresh seats, because QR codes has been attached
            self._send_summaries(appointment.seats.all())

        if getattr(appointment, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the appointment.
            appointment._prefetched_objects_cache = {}

        return Response(serializer.data)

    def _make_qrs(self, seats):
        for seat in seats:
            m.QRCode.objects.create(seat=seat)

    def _send_summaries(self, seats):
        seat_count = len(seats)
        for seat in seats:
            if not seat.email:
                raise ValidationError({"email": "Email field is required"})
            email.send_qrcode(seat, seat_count)


class SeatViewSet(NoReadModelViewSet):
    queryset = m.Seat.objects.all()
    serializer_class = s.SeatSerializer
    authentication_classes = [auth.AppointmentAuthentication]
    permission_classes = [permissions.AppointmentPermission]

    def has_object_permission(self, request, view, obj):
        return request.appointment == obj.appointment

    def perform_destroy(self, seat):
        if seat.appointment.seats.count() == 1:
            raise ValidationError({api_settings.NON_FIELD_ERRORS_KEY: _("Last Seat can not be deleted")})

        super().perform_destroy(seat)

        time_slot = seat.appointment.time_slot
        if time_slot:
            time_slot.add_usage(-1)


class QRCodeView(generics.GenericAPIView):
    queryset = m.QRCode.objects.all()
    lookup_field = "code"

    def get(self, request, *args, **kwargs):
        error_message = _("This QR code has no associated Seat!")
        # request.auth is set only on Token authentication
        # When logged in through the api browser, only request.user will be set
        token_authenticated = request.auth is not None

        # Nothing to see here. A non-admin user should not be able to do anything with this!
        if not token_authenticated and not request.user.is_authenticated:
            return redirect(settings.FRONTEND_URL)

        qr = self.get_object()

        # the ?format=api or ?format=json URL query parameter will be set
        # when using the top right dropdown button next "GET"
        api_browser_format_param = "format" in request.GET

        if token_authenticated or api_browser_format_param:
            if qr.seat is None:
                raise NotFound(error_message)

            seat_staff_api_url = reverse("staff-seat-detail", args=[qr.seat.pk])
            if request.query_params:
                seat_staff_api_url += "?" + urlencode(request.query_params)
            return redirect(seat_staff_api_url)

        if qr.seat is None:
            messages.error(request, error_message)
            return redirect(django_reverse("admin:appointments_qrcode_change", kwargs={"object_id": qr.pk}))

        # Redirect the logged-in user to the Seat admin page
        return redirect(django_reverse("admin:appointments_seat_change", kwargs={"object_id": qr.seat.pk}))


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = s.VerifyEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK,)


class ResendVerifyEmailView(generics.CreateAPIView):
    serializer_class = s.ResendEmailVerificationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ev = m.EmailVerification.objects.get(pk=serializer.validated_data["uuid"])
        address = ev.appointment.email
        token = ev.make_token()
        email.send_verification(token, address)
        return Response({"success": True, "email": address})


class TimeSlotViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = m.TimeSlot.objects.filter(is_active=True)
    serializer_class = s.TimeSlotSerializer
    filterset_class = f.TimeSlotFilter

    def get_queryset(self):
        return super().get_queryset().filter(start__gt=timezone.now())

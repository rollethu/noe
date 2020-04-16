from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from . import models as m
from . import serializers as s


class LocationViewSet(viewsets.ModelViewSet):
    queryset = m.Location.objects.all()
    serializer_class = s.LocationSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = m.Appointment.objects.all()
    serializer_class = s.AppointmentSerializer


class SeatViewSet(viewsets.ModelViewSet):
    queryset = m.Seat.objects.all()
    serializer_class = s.SeatSerializer


@api_view(http_method_names=["POST"])
def verify_email(request):
    return Response(
        {
            "appointment_url": "https://noe.rollet.app/api/appointments/asdfasdf-1231231-12312-12",
            "appointmen_email": "user@rollet.app",
        }
    )

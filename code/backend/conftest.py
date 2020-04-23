import datetime as dt
from django.conf import settings
from pathlib import Path
from rest_framework.test import APIRequestFactory, APIClient
import pytest
from appointments.models import Location, Appointment, Seat, QRCode


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def location_no_db():
    return Location()


@pytest.fixture
def location():
    return Location.objects.create()


@pytest.fixture
def location2():
    return Location.objects.create()


@pytest.fixture
def appointment():
    return Appointment.objects.create()


@pytest.fixture
def seat(appointment):
    return Seat.objects.create(birth_date=dt.date(1990, 6, 14), appointment=appointment)


@pytest.fixture
def qr(seat):
    return QRCode.objects.create(seat=seat)


@pytest.fixture
def datadir(request):
    return Path(request.fspath.dirname) / "data"

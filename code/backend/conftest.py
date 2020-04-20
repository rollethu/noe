import datetime as dt

import pytest
from rest_framework.test import APIRequestFactory, APIClient

from appointments.models import Location, Appointment, Seat


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

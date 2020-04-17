import datetime as dt

import pytest
from rest_framework.test import APIRequestFactory, APIClient

import appointments.models


@pytest.fixture
def factory():
    return APIRequestFactory()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def appointment():
    return appointments.models.Appointment.objects.create()


@pytest.fixture
def seat(appointment):
    return appointments.models.Seat.objects.create(birth_date=dt.date(1990, 6, 14), appointment=appointment)

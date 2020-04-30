import datetime as dt

import pytest
from django.utils import timezone
from django.utils.timezone import make_aware as maw
from rest_framework import status
from rest_framework.reverse import reverse

from appointments import models as m
from appointments import utils as u


def _make_create_seat_request_body(appointment, extra=None):
    request_body = {
        "appointment": reverse("appointment-detail", kwargs={"pk": appointment.pk}),
        "full_name": "Full Name",
        "birth_date": "1990-06-14",
        "post_code": "1234",
        "city": "Budapest",
        "address_line1": "Alpha street 8.",
        "identity_card_number": "123456AB",
        "email": "asd@asd.com",
    }
    if extra:
        request_body.update(extra)
    return request_body


@pytest.mark.skip("doctor referral is temporarily disabled")
@pytest.mark.django_db
def test_healthcare_number_is_required_if_has_referral(api_client, appointment):
    rv = api_client.post(
        reverse("seat-list"), _make_create_seat_request_body(appointment, {"has_doctor_referral": True}),
    )
    assert rv.status_code == status.HTTP_400_BAD_REQUEST
    assert "healthcare_number" in rv.data


@pytest.mark.django_db
def test_healthcare_number_is_not_required_without_has_referral(api_client, appointment):
    rv = api_client.post(reverse("seat-list"), _make_create_seat_request_body(appointment))
    assert rv.status_code == status.HTTP_201_CREATED
    assert m.Seat.objects.count() == 1


@pytest.mark.django_db
def test_birth_date_cant_be_in_future(api_client, appointment, monkeypatch):
    monkeypatch.setattr(timezone, "now", lambda: maw(dt.datetime(2020, 1, 1, 12)))
    now = timezone.now()
    rv = api_client.post(
        reverse("seat-list"), _make_create_seat_request_body(appointment, {"birth_date": "2020-01-02"})
    )
    assert rv.status_code == status.HTTP_400_BAD_REQUEST
    assert "birth_date" in rv.data


@pytest.mark.django_db
def test_phone_number_normalization(api_client, appointment, monkeypatch):
    monkeypatch.setattr(timezone, "now", lambda: maw(dt.datetime(2020, 1, 1, 12)))
    now = timezone.now()
    rv = api_client.post(
        reverse("seat-list"), _make_create_seat_request_body(appointment, {"phone_number": "06201231234"})
    )
    assert rv.status_code == status.HTTP_201_CREATED
    seat = m.Seat.objects.first()
    assert seat.phone_number == "+36 20 123 1234"


@pytest.mark.django_db
def test_invalid_phone_number(api_client, appointment, monkeypatch):
    monkeypatch.setattr(timezone, "now", lambda: maw(dt.datetime(2020, 1, 1, 12)))
    now = timezone.now()
    rv = api_client.post(
        reverse("seat-list"), _make_create_seat_request_body(appointment, {"phone_number": "0620123"})
    )
    assert rv.status_code == status.HTTP_400_BAD_REQUEST
    assert "phone_number" in rv.data


@pytest.mark.django_db
def test_can_not_delete_last_seat(api_client, seat):
    rv = api_client.delete(reverse("seat-detail", kwargs={"pk": seat.pk}))
    assert rv.status_code == status.HTTP_400_BAD_REQUEST
    assert rv.data["non_field_errors"] == "Az utolsó személy nem törölhető"


@pytest.mark.parametrize(
    "input_value, expected",
    [
        ("", False),
        ("1", False),
        ("12345678", False),
        ("123456789", True),
        ("1234A6789", False),
        ("1234567890", False),
        ("123-456-789", False),
    ],
)
def test_healthcare_number_format_validation(input_value, expected):
    assert u.is_healthcare_number_valid(input_value) == expected


@pytest.mark.django_db
def test_api_error_with_invalid_healthcare_number(api_client, appointment):
    rv = api_client.post(
        reverse("seat-list"), _make_create_seat_request_body(appointment, {"healthcare_number": "123"})
    )
    assert rv.status_code == status.HTTP_400_BAD_REQUEST
    assert rv.data["healthcare_number"] == ["Érvénytelen formátum"]

    rv = api_client.post(
        reverse("seat-list"), _make_create_seat_request_body(appointment, {"healthcare_number": "123456789"})
    )
    assert rv.status_code == status.HTTP_201_CREATED

    rv = api_client.post(reverse("seat-list"), _make_create_seat_request_body(appointment, {"healthcare_number": ""}))
    assert rv.status_code == status.HTTP_201_CREATED

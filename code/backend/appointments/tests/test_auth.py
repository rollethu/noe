from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
import pytest
from .. import models as m


SEAT_DETAILS = {
    "full_name": "Test name",
    "birth_date": "1988-03-02",
    "identity_card_number": "123456789",
    "post_code": "1234",
    "city": "Budapest",
    "address_line1": "Street 11",
    "email": "test@rollet.app",
}


def test_api_cannot_be_reached_without_Authorization_header(api_client):
    res = api_client.post("/api/seats/")
    # because we don't implement .authenticate_header()
    # Otherwise it would be 401
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_invalid_auth_header_token(api_client):
    api_client.credentials(HTTP_AUTHORIZATION=f"Apptoken non-base64-token")
    res = api_client.post("/api/seats/")
    assert res.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_appointment_cannot_be_changed_with_another_appointment_token(
    appointment, appointment_client, appointment_client2, api_client
):
    appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
    res = appointment_client.patch(appointment_url, {"is_registration_finished": True})
    assert res.status_code == status.HTTP_200_OK

    res2 = appointment_client2.patch(appointment_url, {"is_registration_finished": False})
    assert res2.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_seat_cannot_be_created_with_another_appointment_token(
    appointment, appointment_client, appointment_client2, api_client
):
    appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
    request_body = {
        "appointment": appointment_url,
        **SEAT_DETAILS,
    }
    res = appointment_client.post("/api/seats/", request_body)
    assert res.status_code == status.HTTP_201_CREATED

    res2 = appointment_client2.post("/api/seats/", request_body)
    assert res2.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_seat_cannot_be_changed_with_another_appointment_token(
    appointment, appointment_client, appointment_client2, api_client
):
    appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
    request_body = {
        "appointment": appointment_url,
        **SEAT_DETAILS,
    }
    seat = m.Seat.objects.create(appointment=appointment, **SEAT_DETAILS)
    seat_url = reverse("seat-detail", kwargs={"pk": seat.pk})
    res = appointment_client.patch(seat_url, request_body)
    assert res.status_code == status.HTTP_200_OK

    res2 = appointment_client2.patch(seat_url, request_body)
    assert res2.status_code == status.HTTP_403_FORBIDDEN

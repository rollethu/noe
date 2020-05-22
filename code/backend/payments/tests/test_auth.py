from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
import pytest
from appointments.models import Appointment, Seat
from ..prices import ProductType, PaymentMethodType


@pytest.mark.django_db
def test_get_price_cannot_be_called_with_different_appointment_token(
    appointment, appointment_client, appointment_client2
):
    appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
    request_body = {
        "appointment": appointment_url,
        "product_type": ProductType.NORMAL_EXAM,
    }
    res = appointment_client.post("/api/get-price/", request_body)
    assert res.status_code == status.HTTP_200_OK

    res2 = appointment_client2.post("/api/get-price/", request_body)
    assert res2.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_pay_appointment_cannot_be_called_with_different_appointment_token(appointment, appointment_client2):
    Seat.objects.create(appointment=appointment, birth_date=timezone.now())
    appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
    request_body = {
        "appointment": appointment_url,
        "product_type": ProductType.NORMAL_EXAM,
        "payment_method": PaymentMethodType.ON_SITE,
        "total_price": 24_980,
        "currency": "HUF",
    }
    res = appointment_client2.post("/api/pay-appointment/", request_body)
    assert res.status_code == status.HTTP_403_FORBIDDEN

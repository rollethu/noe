import pytest
from django.utils import timezone
from django.urls import reverse
from rest_framework import status

from appointments import models as am


@pytest.mark.django_db
def test_validation_error_with_wrong_paid_at(client, admin_user, seat, payment):
    assert payment.seat == seat
    payment.paid_at = timezone.now()
    payment.save()

    qrcode = am.QRCode.objects.create(seat=seat)

    url = reverse("admin:appointments_seat_change", args=(seat.pk,))
    relevant_form_data = {
        "payment-0-paid_at_0": "2020.05.13.",
        "payment-0-paid_at_1": "10:15:12",
    }
    request_data = {
        "full_name": "Teszt User 1",
        "birth_date": "0123.12.03.",
        "identity_card_number": "123123AB",
        "healthcare_number": "",
        "doctor_name": "",
        "phone_number": "+36 1 123 1231",
        "email": "asd@asd.com",
        "post_code": "1111",
        "city": "Budapest",
        "address_line1": "Yolo utca 13",
        "address_line2": "",
        "sample_set-TOTAL_FORMS": "1",
        "sample_set-INITIAL_FORMS": "0",
        "sample_set-MIN_NUM_FORMS": "0",
        "sample_set-MAX_NUM_FORMS": "1000",
        "sample_set-0-uuid": "",
        "sample_set-0-seat": seat.pk,
        "sample_set-0-sampled_at_0": "2020.05.13.",
        "sample_set-0-sampled_at_1": "13:04:54",
        "initial-sample_set-0-sampled_at_0": "2020.05.13.",
        "initial-sample_set-0-sampled_at_1": "13:04:54",
        "sample_set-0-vial": "",
        "sample_set-__prefix__-uuid": "",
        "sample_set-__prefix__-seat": seat.pk,
        "sample_set-__prefix__-sampled_at_0": "2020.05.13.",
        "sample_set-__prefix__-sampled_at_1": "13:04:54",
        "initial-sample_set-__prefix__-sampled_at_0": "2020.05.13.",
        "initial-sample_set-__prefix__-sampled_at_1": "13:04:54",
        "sample_set-__prefix__-vial": "",
        "payment-TOTAL_FORMS": "1",
        "payment-INITIAL_FORMS": "1",
        "payment-MIN_NUM_FORMS": "0",
        "payment-MAX_NUM_FORMS": "1",
        "payment-0-proof_number": "",
        "payment-0-note": "",
        "payment-0-uuid": payment.pk,
        "payment-0-seat": seat.pk,
        "payment-__prefix__-paid_at_0": "",
        "payment-__prefix__-paid_at_1": "",
        "payment-__prefix__-proof_number": "",
        "payment-__prefix__-note": "",
        "payment-__prefix__-uuid": "",
        "payment-__prefix__-seat": seat.pk,
        "qrcode-TOTAL_FORMS": "1",
        "qrcode-INITIAL_FORMS": "1",
        "qrcode-MIN_NUM_FORMS": "0",
        "qrcode-MAX_NUM_FORMS": "1",
        "qrcode-0-id": qrcode.pk,
        "qrcode-0-seat": seat.pk,
        "qrcode-__prefix__-id": "",
        "qrcode-__prefix__-seat": seat.pk,
        "_save": "Mentés",
    }
    request_data.update(relevant_form_data)
    client.login(username="admin", password="asdasdasd")
    response = client.post(url, request_data)
    assert response.status_code == status.HTTP_200_OK
    assert "Paid at can not be changed" in response.context["errors"][0]

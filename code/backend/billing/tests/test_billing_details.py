import pytest
from rest_framework import status
from rest_framework.test import force_authenticate

from appointments.models import Seat, EmailVerification
from billing import models as bm
from payments.prices import ProductType
from payments.views import PayAppointmentView


pay_appointment_view = PayAppointmentView.as_view()


def _authenticate_appointment(request, appointment):
    ev = EmailVerification.objects.create(appointment=appointment)
    force_authenticate(request, token=appointment)


@pytest.mark.django_db
def test_billing_details_creation(factory, appointment, appointment_url, seat):
    assert not bm.BillingDetail.objects.exists()
    total_price = 26_990
    request = factory.post(
        "/api/pay-appointment/",
        {
            "appointment": appointment_url,
            "product_type": ProductType.NORMAL_EXAM,
            "total_price": total_price,
            "currency": "HUF",
            "company_name": "Fake Company",
            "country": "Fake Country",
            "address_line1": "Fake Address Line 1",
            "post_code": "1234",
            "city": "Budapest",
            "tax_number": "123456789",
        },
    )
    _authenticate_appointment(request, appointment)
    response = pay_appointment_view(request)
    assert response.status_code == status.HTTP_200_OK, response.data
    assert bm.BillingDetail.objects.exists()
    bd = bm.BillingDetail.objects.first()
    assert bd.appointment == appointment
    assert bd.company_name == "Fake Company"
    assert bd.country == "Fake Country"
    assert bd.address_line1 == "Fake Address Line 1"
    assert bd.post_code == "1234"
    assert bd.city == "Budapest"
    assert bd.tax_number == "123456789"

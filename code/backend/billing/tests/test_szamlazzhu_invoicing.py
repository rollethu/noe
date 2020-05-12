import pytest

from appointments import models as am
from billing import models as m
from billing import services
from payments import models as pm
from payments.prices import PRODUCTS, ProductType


@pytest.mark.vcr()
@pytest.mark.django_db
def test_sending_invoice(appointment, seat):
    appointment.email = "test@rollet.app"
    appointment.save()
    payment = pm.Payment.objects.create(
        seat=seat, amount=1000, currency="HUF", product_type=PRODUCTS[ProductType.NORMAL_EXAM].product_type
    )
    billing_details = m.BillingDetail.objects.create(
        company_name="Test Company",
        appointment=appointment,
        city="Budapest",
        post_code="1234",
        address_line1="Fake street 13",
        tax_number="123456789",
    )
    appointment.refresh_from_db()
    seat.refresh_from_db()
    services.send_invoice(seat)

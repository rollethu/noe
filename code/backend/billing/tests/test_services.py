import os
from decimal import Decimal
from unittest.mock import Mock
import pytest
from online_payments.billing.szamlazzhu import Szamlazzhu
from online_payments.billing.models import Item, Invoice, Customer, VATRate, PaymentMethod
from appointments.models import Appointment, Seat
from payments.models import Payment
from payments.prices import ProductType
from billing.models import BillingDetail
from billing.services import send_invoice


@pytest.mark.django_db
class TestSendInvoice:
    def test_send_invoice_called(self, monkeypatch, billing_detail):
        mock_send = Mock()
        monkeypatch.setattr(Szamlazzhu, "send_invoice", mock_send)

        email = "test@rollet.app"
        full_name = "Test User"
        amount = 100

        appointment = Appointment(email=email, billing_detail=billing_detail)
        seat = Seat(
            full_name=full_name,
            payment=Payment(amount=amount, product_type=ProductType.NORMAL_EXAM),
            appointment=appointment,
        )
        send_invoice(seat)

        item = Item(
            name="NORMAL_EXAM",
            quantity=1,
            unit="db",
            net_unit_price=Decimal("79"),
            net_price=Decimal("79"),
            vat_rate=VATRate.PERCENT_27,
            vat_value=Decimal("21"),
            gross_price=100,
        )
        customer = Customer(
            name="Test Company",
            address="Test street 11.",
            post_code="1234",
            city="Budapest",
            tax_number="123456789",
            email=email,
        )
        invoice = Invoice(items=[item], payment_method=PaymentMethod.CREDIT_CARD, customer=customer)
        mock_send.assert_called_once_with(invoice, os.environ["SZAMLAZZHU_INVOICE_PREFIX"])

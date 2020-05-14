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

        item1 = Item(
            name="Laboratóriumi teszt - Alapcsomag (72 óra)",
            quantity=1,
            unit="db",
            net_price=17_000,
            net_unit_price=17_000,
            vat_rate=VATRate.PERCENT_0,
            vat_value=0,
            gross_price=17_000,
        )

        item2 = Item(
            name="Mintavételi csomag",
            quantity=1,
            unit="db",
            net_price=9514,
            net_unit_price=9514,
            vat_rate=VATRate.PERCENT_5,
            vat_value=476,
            gross_price=9_990,
        )

        customer = Customer(
            name="Test Company",
            address="Test street 11.",
            post_code="1234",
            city="Budapest",
            tax_number="123456789",
            email=email,
        )
        invoice = Invoice(items=[item1, item2], payment_method=PaymentMethod.CREDIT_CARD, customer=customer)
        mock_send.assert_called_once_with(invoice, os.environ["SZAMLAZZHU_INVOICE_PREFIX"])

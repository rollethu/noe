import os
from typing import List
from collections import defaultdict
import logging
from django.conf import settings
from online_payments.billing.enums import Currency
from online_payments.billing.models import Item, PaymentMethod, Invoice, Customer
from online_payments.billing.szamlazzhu import Szamlazzhu
from payments.prices import PRODUCTS, get_product_items
from .interface import BillingService

logger = logging.getLogger(__name__)


class SzamlazzhuService(BillingService):
    """
    Uses Rollet proprietary online_payments package,
    which uses szamlazz.hu billing provider to send invoices on payments.
    """

    def __init__(self):
        self._szamlazzhu = Szamlazzhu(os.environ["SZAMLAZZHU_AGENT_KEY"], Currency.HUF)

    def send_seat_invoice(self, seat):
        self._send_invoice(seat.appointment.billing_detail, seat.appointment.email, self._get_items_for_seats([seat]))

    def send_appointment_invoice(self, appointment):
        self._send_invoice(
            appointment.billing_detail, appointment.email, self._get_items_for_seats(appointment.seats.all())
        )

    def _get_items_for_seats(self, seats) -> List[Item]:
        grouped_products = defaultdict(int)
        for seat in seats:
            grouped_products[seat.payment.product_type] += 1

        items = []
        for product_type, quantity in grouped_products.items():
            items.extend(get_product_items(PRODUCTS[product_type], quantity))

        return items

    def _send_invoice(self, billing_detail, email, items):
        customer = Customer(
            name=billing_detail.company_name,
            post_code=billing_detail.post_code,
            city=billing_detail.city,
            address=billing_detail.address_line1,
            email=email,
            tax_number=billing_detail.tax_number,
        )
        invoice = Invoice(items=items, payment_method=PaymentMethod.CREDIT_CARD, customer=customer)
        logger.info("Sending invoice to: %s", email)
        self._szamlazzhu.send_invoice(invoice, os.environ["SZAMLAZZHU_INVOICE_PREFIX"])

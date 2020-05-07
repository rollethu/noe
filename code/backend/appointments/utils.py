import re

from django.conf import settings
from online_payments.billing.enums import Currency
from online_payments.billing.models import Item, Receipt, PaymentMethod
from online_payments.billing.szamlazzhu.client import Szamlazzhu

from payments.prices import PRODUCTS


def is_healthcare_number_valid(value):
    pattern = re.compile("[0-9]{9}")
    print(pattern, value, pattern.match(value))
    return pattern.fullmatch(value) is not None


def send_bill_to_seat(seat):
    if seat.appointment.request_vat_invoice:
        send_invoice_to_seat(seat)
    else:
        send_receipt_to_seat(seat)


def send_invoice_to_seat(seat):
    pass


def send_receipt_to_seat(seat):
    product = PRODUCTS[seat.payment.product_type]

    net_price = product.amount / 1.27
    vat_value = product.amount - net_price
    receipt_item = Item(
        name=product.product_type,
        quantity=1,
        unit="db",
        net_unit_price=net_price,
        net_price=net_price,
        vat_rate=27,
        vat_value=vat_value,
        gross_price=product.amount,
    )
    receipt = Receipt(items=[receipt_item], payment_method=PaymentMethod.CREDIT_CARD)
    szamlazzhu = Szamlazzhu(invoice_agent_key=settings.SZAMLAZZHU_AGENT_KEY, currency=Currency.HUF)
    szamlazzhu.send_receipt(receipt, prefix=settings.SZAMLAZZ_HU_RECEIPT_PREFIX)

    seat.payment.bill_id = receipt.receipt_id
    seat.payment.save()

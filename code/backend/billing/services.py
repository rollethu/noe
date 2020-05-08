
from django.conf import settings
from online_payments.billing.enums import Currency, VATRate
from online_payments.billing.models import Item, Receipt, PaymentMethod, Invoice, Customer
from online_payments.billing.szamlazzhu.client import Szamlazzhu

from . import models as m
from payments.prices import PRODUCTS






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
        quantity=str(1),
        unit="db",
        net_unit_price=str(net_price),
        net_price=str(net_price),
        vat_rate=str(27),
        vat_value=str(vat_value),
        gross_price=str(product.amount),
    )
    receipt = Receipt(items=[receipt_item], payment_method=PaymentMethod.CREDIT_CARD)
    szamlazzhu = Szamlazzhu(invoice_agent_key=settings.SZAMLAZZHU_AGENT_KEY, currency=Currency.HUF)
    szamlazzhu.send_receipt(receipt, prefix=settings.SZAMLAZZ_HU_RECEIPT_PREFIX)



def send_invoice_to_seat(seat):
    product = PRODUCTS[seat.payment.product_type]
    net_price = product.amount / 1.27
    vat_value = product.amount - net_price
    invoice_item = Item(
        name=product.product_type,
        quantity=str(1),
        unit="db",
        net_unit_price=str(net_price),
        net_price=str(net_price),
        vat_rate=VATRate.PERCENT_27,
        vat_value=str(vat_value),
        gross_price=str(product.amount),
    )
    customer = Customer(
        name=seat.appointment.billing_detail.company_name,
        post_code=seat.appointment.billing_detail.post_code,
        city=seat.appointment.billing_detail.city,
        address=seat.appointment.billing_detail.address_line1,
        email=seat.appointment.email,
        tax_number=seat.appointment.billing_detail.tax_number,
    )
    invoice = Invoice(items=[invoice_item], payment_method=PaymentMethod.CREDIT_CARD, customer=customer)
    szamlazzhu = Szamlazzhu(settings.SZAMLAZZHU_AGENT_KEY, Currency.HUF)
    szamlazzhu.send_invoice(invoice, settings.SZAMLAZZHU_INVOICE_PREFIX)

    m.Bill(appointment=seat.appointment, payment=seat.payment, bill_type=m.Bill.BILL_TYPE_VAT_INVOICE, bill_id=invoice.invoice_id, )

from decimal import Decimal, ROUND_HALF_UP
from django.conf import settings
from online_payments.billing.enums import Currency, VATRate
from online_payments.billing.models import Item, Receipt, PaymentMethod, Invoice, Customer
from online_payments.billing.szamlazzhu import Szamlazzhu
from payments.prices import round_price, PRODUCTS
from . import models as m


def send_invoice(seat):
    appointment, payment = seat.appointment, seat.payment
    net_price = payment.amount / Decimal("1.27")
    rounded_net_price = round_price(net_price, payment.currency)
    vat_value = payment.amount - rounded_net_price

    product = PRODUCTS[payment.product_type]
    billing_detail = appointment.billing_detail
    customer = Customer(
        name=billing_detail.company_name,
        post_code=billing_detail.post_code,
        city=billing_detail.city,
        address=billing_detail.address_line1,
        email=appointment.email,
        tax_number=billing_detail.tax_number,
    )
    invoice = Invoice(items=product.items, payment_method=PaymentMethod.CREDIT_CARD, customer=customer)
    szamlazzhu = Szamlazzhu(settings.SZAMLAZZHU_AGENT_KEY, Currency.HUF)
    szamlazzhu.send_invoice(invoice, settings.SZAMLAZZHU_INVOICE_PREFIX)

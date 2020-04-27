import enum
from dataclasses import dataclass
from django.utils.translation import gettext as _
from . import models as m


class PaymentMethodType:
    SIMPLEPAY = "SIMPLEPAY"
    ON_SITE = "ON_SITE"


class ProductType:
    DOCTOR_REFERRAL = "DOCTOR_REFERRAL"
    NORMAL_EXAM = "NORMAL_EXAM"
    PRIORITY_EXAM = "PRIORITY_EXAM"
    PRIORITY_EXAM_FRADI = "PRIORITY_EXAM_FRADI"


PAYMENT_METHOD_TYPE_CHOICES = (
    (PaymentMethodType.SIMPLEPAY, _("SimplePay")),
    (PaymentMethodType.ON_SITE, _("On-site")),
)

PRODUCT_CHOICES = (
    # DOCTOR_REFERRAL is dynamically chosen based on Seat.has_doctor_referral, not needed here
    (ProductType.NORMAL_EXAM, _("Normál vizsgálat")),
    (ProductType.PRIORITY_EXAM, _("Elsőbbségi vizsgálat")),
    (ProductType.PRIORITY_EXAM_FRADI, _("Elsőbbségi vizsgálat Fradi Szurkolói Kártya kedvezménnyel")),
)


@dataclass
class Product:
    product_type: str
    amount: float
    currency: str
    payment_method_type: str


PRODUCTS = {
    ProductType.DOCTOR_REFERRAL: Product(ProductType.DOCTOR_REFERRAL, 0, "HUF", PaymentMethodType.ON_SITE),
    ProductType.NORMAL_EXAM: Product(ProductType.NORMAL_EXAM, 26_990, "HUF", PaymentMethodType.ON_SITE),
    ProductType.PRIORITY_EXAM: Product(ProductType.PRIORITY_EXAM, 36_990, "HUF", PaymentMethodType.ON_SITE),
    ProductType.PRIORITY_EXAM_FRADI: Product(
        ProductType.PRIORITY_EXAM_FRADI, 33_500, "HUF", PaymentMethodType.ON_SITE
    ),
}


def calc_payments(seats, product: Product):
    payments = []

    for seat in seats:
        if seat.has_doctor_referral:
            current_product = PRODUCTS[ProductType.DOCTOR_REFERRAL]
        else:
            current_product = product

        p = m.Payment(
            seat=seat,
            amount=current_product.amount,
            currency=current_product.currency,
            product_type=current_product.product_type,
            payment_method_type=current_product.payment_method_type,
        )

        payments.append(p)

    summary = {
        "total_price": sum(p.amount for p in payments),
        "currency": "HUF",
    }

    return payments, summary

import enum
from typing import List
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from django.utils.translation import gettext as _
from online_payments.billing import Item as BillingItem, VATRate
from . import models as m
from feature_flags import use_feature_simplepay


class PaymentMethodType:
    SIMPLEPAY = "SIMPLEPAY"
    ON_SITE = "ON_SITE"


class ProductType:
    DOCTOR_REFERRAL = "DOCTOR_REFERRAL"
    NORMAL_EXAM = "NORMAL_EXAM"
    PRIORITY_EXAM = "PRIORITY_EXAM"
    # PRIORITY_EXAM_FRADI = "PRIORITY_EXAM_FRADI"


PAYMENT_METHOD_TYPE_CHOICES = ((PaymentMethodType.ON_SITE, _("On-site")),)

if use_feature_simplepay:
    PAYMENT_METHOD_TYPE_CHOICES += ((PaymentMethodType.SIMPLEPAY, _("SimplePay")),)

PRODUCT_CHOICES = (
    # DOCTOR_REFERRAL is dynamically chosen based on Seat.has_doctor_referral, not needed here
    (ProductType.NORMAL_EXAM, _("Normál vizsgálat")),
    (ProductType.PRIORITY_EXAM, _("Elsőbbségi vizsgálat")),
    # (ProductType.PRIORITY_EXAM_FRADI, _("Elsőbbségi vizsgálat Fradi Szurkolói Kártya kedvezménnyel")),
)


@dataclass
class Product:
    product_type: str
    amount: float
    currency: str
    payment_method_type: str
    item_classes: List


@dataclass
class _ItemBase:
    name: str
    net_unit_price: Decimal
    gross_unit_price: Decimal
    unit_vat_value: Decimal
    vat_rate: VATRate
    unit: str = "db"


class NormalTest(_ItemBase):
    name = _("Laboratóriumi teszt - Alapcsomag (72 óra)")
    net_unit_price = 17_000
    gross_unit_price = 17_000
    unit_vat_value = 0
    vat_rate = VATRate.PERCENT_0


class PriorityTest(_ItemBase):
    name = _("Laboratóriumi teszt - Elsőbbségi (1 nap)")
    net_unit_price = 17_000
    gross_unit_price = 17_000
    unit_vat_value = 0
    vat_rate = VATRate.PERCENT_0


class NormalPackage(_ItemBase):
    name = _("Mintavételi csomag")
    vat_rate = VATRate.PERCENT_5
    net_unit_price = 7_600
    gross_unit_price = 7_980
    unit_vat_value = 380


class PriorityPackage(_ItemBase):
    name = _("Mintavételi csomag")
    vat_rate = VATRate.PERCENT_5
    net_unit_price = 19_038
    gross_unit_price = 19_990
    unit_vat_value = 952


PRODUCTS = {
    ProductType.DOCTOR_REFERRAL: Product(
        ProductType.DOCTOR_REFERRAL, 0, "HUF", PaymentMethodType.ON_SITE, item_classes=[]
    ),
    ProductType.NORMAL_EXAM: Product(
        ProductType.NORMAL_EXAM, 24_980, "HUF", PaymentMethodType.ON_SITE, item_classes=[NormalTest, NormalPackage],
    ),
    ProductType.PRIORITY_EXAM: Product(
        ProductType.PRIORITY_EXAM,
        36_990,
        "HUF",
        PaymentMethodType.ON_SITE,
        item_classes=[PriorityTest, PriorityPackage],
    ),
}


def get_product_items(product: Product, quantity: int) -> List[BillingItem]:
    return [
        BillingItem(
            name=item_class.name,
            quantity=quantity,
            unit=item_class.unit,
            net_unit_price=item_class.net_unit_price,
            net_price=item_class.net_unit_price * quantity,
            gross_price=item_class.gross_unit_price * quantity,
            vat_value=item_class.unit_vat_value,
            vat_rate=item_class.vat_rate,
        )
        for item_class in product.item_classes
    ]


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


def round_price(amount, currency):
    if currency == "HUF":
        precision = Decimal("0")
    else:
        precision = Decimal("0.01")
    return amount.quantize(precision, rounding=ROUND_HALF_UP)

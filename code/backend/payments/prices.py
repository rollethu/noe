import enum
from typing import List
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from django.utils.translation import gettext as _
from online_payments.billing import Item as BillingItem, VATRate
from . import models as m


class PaymentMethodType:
    SIMPLEPAY = "SIMPLEPAY"
    ON_SITE = "ON_SITE"


class ProductType:
    DOCTOR_REFERRAL = "DOCTOR_REFERRAL"
    NORMAL_EXAM = "NORMAL_EXAM"
    PRIORITY_EXAM = "PRIORITY_EXAM"
    # PRIORITY_EXAM_FRADI = "PRIORITY_EXAM_FRADI"


PAYMENT_METHOD_TYPE_CHOICES = (
    (PaymentMethodType.SIMPLEPAY, _("SimplePay")),
    (PaymentMethodType.ON_SITE, _("On-site")),
)

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


class _BaseItem:
    unit = "db"
    name = ""
    net_unit_price = ""
    gross_unit_price = ""
    unit_vat_value = ""
    vat_rate = ""

    def __init__(self, quantity: int):
        self.unit = self.unit
        self.name = self.name
        self.vat_rate = self.vat_rate
        self.net_unit_price = self.net_unit_price

        self.quantity = quantity
        self.net_price = self.net_unit_price * quantity
        self.gross_price = self.gross_unit_price * quantity
        self.vat_value = self.unit_vat_value * quantity


class ProductPackage(_BaseItem):
    name = _("Laboratóriumi teszt")
    net_unit_price = 17_000
    gross_unit_price = 17_000
    unit_vat_value = 0
    vat_rate = VATRate.PERCENT_0


class NormalProductPackage(ProductPackage):
    name = _("Laboratóriumi teszt - Alapcsomag (72 óra)")


class PriorityProductPackage(NormalProductPackage):
    name = _("Laboratóriumi teszt - Elsőbbségi (1 nap)")


class ServicePackage(_BaseItem):
    name = _("Mintavételi csomag")
    vat_rate = VATRate.PERCENT_5


class NormalServicePackage(ServicePackage):
    net_unit_price = 7_600
    gross_unit_price = 7_980
    unit_vat_value = 380


class PriorityServicePackage(ServicePackage):
    net_unit_price = 19_038
    gross_unit_price = 19_990
    unit_vat_value = 952


PRODUCTS = {
    ProductType.DOCTOR_REFERRAL: Product(
        ProductType.DOCTOR_REFERRAL, 0, "HUF", PaymentMethodType.ON_SITE, item_classes=[]
    ),
    ProductType.NORMAL_EXAM: Product(
        ProductType.NORMAL_EXAM,
        24_980,
        "HUF",
        PaymentMethodType.ON_SITE,
        item_classes=[NormalProductPackage, NormalServicePackage],
    ),
    ProductType.PRIORITY_EXAM: Product(
        ProductType.PRIORITY_EXAM,
        36_990,
        "HUF",
        PaymentMethodType.ON_SITE,
        item_classes=[PriorityProductPackage, PriorityServicePackage],
    ),
}


def get_product_items(product: Product, quantity: int) -> List[BillingItem]:
    return [BillingItem(**item_class(quantity).__dict__) for item_class in product.item_classes]


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

import enum
from dataclasses import dataclass
from django.utils.translation import gettext as _


class PaymentMethodType:
    SIMPLEPAY = "SIMPLEPAY"
    ON_SITE = "ON_SITE"


@dataclass
class Price:
    name: str
    amount: float
    currency: str
    payment_method_type: str


DOCTOR_REFERRAL = Price(_("Orvosi beutaló"), 0, "HUF", PaymentMethodType.ON_SITE)

TEST_ONLINE = Price(_("Online fizetés"), 10_000, "HUF", PaymentMethodType.SIMPLEPAY)

TEST_ON_SITE = Price(_("Fizetés a helyszínen bankkártyával"), 12_000, "HUF", PaymentMethodType.ON_SITE)


def calculate_price(seats, payment_method_type: PaymentMethodType):
    prices = []

    for seat in seats:
        if seat.has_doctor_referral:
            prices.append(DOCTOR_REFERRAL)
        elif payment_method_type == PaymentMethodType.ON_SITE:
            prices.append(TEST_ON_SITE)
        elif payment_method_type == PaymentMethodType.SIMPLEPAY:
            prices.append(TEST_ONLINE)

    return {
        "total_price": sum(p.amount for p in prices),
        "currency": "HUF",
    }

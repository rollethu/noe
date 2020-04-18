import enum
from dataclasses import dataclass
from django.utils.translation import gettext as _
from . import models as m


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


def calc_payments(seats, payment_method_type: PaymentMethodType):
    payments = []

    for seat in seats:
        p = m.Payment(seat=seat, payment_method_type=payment_method_type)

        if seat.has_doctor_referral:
            p.amount = DOCTOR_REFERRAL.amount
        elif payment_method_type == PaymentMethodType.ON_SITE:
            p.amount = TEST_ON_SITE.amount
        elif payment_method_type == PaymentMethodType.SIMPLEPAY:
            p.amount = TEST_ONLINE.amount

        payments.append(p)

    summary = {
        "total_price": sum(p.amount for p in payments),
        "currency": "HUF",
    }

    return payments, summary

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

TEST_OFFLINE = Price(_("Fizetés a helyszínen bankkártyával"), 12_000, "HUF", PaymentMethodType.ON_SITE)

import math
from decimal import Decimal, ROUND_HALF_UP
from django import template

register = template.Library()

LOCALIZED_CURRENCIES = {
    "HUF": "Ft",
}


@register.simple_tag
def format_money(amount: Decimal, currency: str):
    if not isinstance(amount, (int, Decimal)):
        raise TypeError(f"Invalid amount: {amount}")

    if not isinstance(currency, str):
        raise TypeError(f"Invalid currency: {currency}")

    try:
        localized_currency = LOCALIZED_CURRENCIES[currency]
    except KeyError:
        raise ValueError(f"Invalid currency: {currency}")

    rounded_amount = Decimal(amount).quantize(Decimal(0), rounding=ROUND_HALF_UP)

    return f"{rounded_amount} {localized_currency}"

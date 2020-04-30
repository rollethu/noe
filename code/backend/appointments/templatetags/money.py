import math
from django import template

register = template.Library()

LOCALIZED_CURRENCIES = {
    "HUF": "Ft",
}


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier


@register.simple_tag
def format_money(amount: int, currency: str):
    if not isinstance(amount, (int, float)):
        raise TypeError(f"Invalid amount: {amount}")

    if not isinstance(currency, str):
        raise TypeError(f"Invalid currency: {currency}")

    try:
        localized_currency = LOCALIZED_CURRENCIES[currency]
    except KeyError:
        raise ValueError(f"Invalid currency: {currency}")

    rounded_amount = int(round_half_up(amount))

    return f"{rounded_amount} {localized_currency}"

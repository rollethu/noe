from decimal import Decimal
import pytest
from ..templatetags.money import format_money


@pytest.mark.parametrize(
    "amount, currency, expected",
    [
        (100, "HUF", "100 Ft"),
        (26_990, "HUF", "26990 Ft"),
        (36_990, "HUF", "36990 Ft"),
        (Decimal("1234.5"), "HUF", "1235 Ft"),
        (Decimal("1234.1"), "HUF", "1234 Ft"),
        (0, "HUF", "0 Ft"),
        (Decimal("0.0"), "HUF", "0 Ft"),
    ],
)
def test_format_money(amount, currency, expected):
    assert format_money(amount, currency) == expected


@pytest.mark.parametrize(
    "amount, currency, exc_type",
    [
        (None, "HUF", TypeError),
        (100, "", ValueError),
        (100, None, TypeError),
        (100, 10, TypeError),
        (None, 10, TypeError),
        ("", "HUF", TypeError),
        ("abc", "HUF", TypeError),
    ],
)
def test_format_money_with_invalid_valu_raises_Exception(amount, currency, exc_type):
    with pytest.raises(exc_type):
        format_money(amount, currency)

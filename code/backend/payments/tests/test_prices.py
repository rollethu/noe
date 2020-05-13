from decimal import Decimal
import pytest
from appointments.models import Seat
from ..prices import calc_payments, PRODUCTS, ProductType, round_price


class TestCalculatePayments:
    def test_zero_seats_has_no_payments(self):
        payments, summary = calc_payments([], PRODUCTS[ProductType.NORMAL_EXAM])
        assert len(payments) == 0
        assert summary == {"total_price": 0, "currency": "HUF"}

    def test_seat_count_is_the_same_as_payment_count(self):
        count = 10
        seats = [Seat() for _ in range(count)]
        payments, _ = calc_payments(seats, PRODUCTS[ProductType.NORMAL_EXAM])
        assert len(payments) == count

    def test_calculate_only_has_doctor_referral(self):
        s1 = Seat(has_doctor_referral=True)
        s2 = Seat(has_doctor_referral=True)
        _, summary = calc_payments([s1, s2], PRODUCTS[ProductType.NORMAL_EXAM])
        assert summary == {
            "total_price": 0,
            "currency": "HUF",
        }

    def test_calculate_NORMAL_PRICE(self):
        s1 = Seat()
        s2 = Seat()
        _, summary = calc_payments([s1, s2], PRODUCTS[ProductType.NORMAL_EXAM])
        assert summary == {
            "total_price": 53_980,
            "currency": "HUF",
        }

    def test_calculate_has_doctor_referral_and_NORMAL_PRICE(self):
        s1 = Seat(has_doctor_referral=True)
        s2 = Seat()
        _, summary = calc_payments([s1, s2], PRODUCTS[ProductType.NORMAL_EXAM])
        assert summary == {
            "total_price": 26_990,
            "currency": "HUF",
        }

    def test_calculate_has_doctor_referral_and_2_ON_SITE(self):
        s1 = Seat(has_doctor_referral=True)
        s2 = Seat()
        s3 = Seat()
        _, summary = calc_payments([s1, s2, s3], PRODUCTS[ProductType.NORMAL_EXAM])
        assert summary == {
            "total_price": 53_980,
            "currency": "HUF",
        }


@pytest.mark.parametrize(
    "amount, currency, expected",
    (
        ("0", "HUF", "0"),
        ("0.00", "HUF", "0"),
        ("5.123", "HUF", "5"),
        ("5.5", "HUF", "6"),
        ("5.623", "HUF", "6"),
        ("0", "USD", "0"),
        ("0.0", "USD", "0"),
        ("0.00", "USD", "0"),
        ("5.623", "USD", "5.62"),
        ("5.625", "USD", "5.63"),
        ("5.636", "EUR", "5.64"),
    ),
)
def test_round_price(amount, currency, expected):
    assert round_price(Decimal(amount), currency) == Decimal(expected)

import pytest
from appointments.models import Seat
from ..prices import calc_payments, PaymentMethodType


class TestCalculatePayments:
    def test_zero_seats_has_no_payments(self):
        payments, summary = calc_payments([], PaymentMethodType.ON_SITE)
        assert len(payments) == 0
        assert summary == {"total_price": 0, "currency": "HUF"}

    def test_seat_count_is_the_same_as_payment_count(self):
        count = 10
        seats = [Seat() for _ in range(count)]
        payments, _ = calc_payments(seats, PaymentMethodType.ON_SITE)
        assert len(payments) == count

    def test_calculate_only_has_doctor_referral(self):
        s1 = Seat(has_doctor_referral=True)
        s2 = Seat(has_doctor_referral=True)
        _, summary = calc_payments([s1, s2], PaymentMethodType.ON_SITE)
        assert summary == {
            "total_price": 0,
            "currency": "HUF",
        }

    def test_calculate_ON_SITE_only(self):
        s1 = Seat()
        s2 = Seat()
        _, summary = calc_payments([s1, s2], PaymentMethodType.ON_SITE)
        assert summary == {
            "total_price": 24_000,
            "currency": "HUF",
        }

    def test_calculate_has_doctor_referral_and_ON_SITE(self):
        s1 = Seat(has_doctor_referral=True)
        s2 = Seat()
        _, summary = calc_payments([s1, s2], PaymentMethodType.ON_SITE)
        assert summary == {
            "total_price": 12_000,
            "currency": "HUF",
        }

    def test_calculate_has_doctor_referral_and_2_ON_SITE(self):
        s1 = Seat(has_doctor_referral=True)
        s2 = Seat()
        s3 = Seat()
        _, summary = calc_payments([s1, s2, s3], PaymentMethodType.ON_SITE)
        assert summary == {
            "total_price": 24_000,
            "currency": "HUF",
        }

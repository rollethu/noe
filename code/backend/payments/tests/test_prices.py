import pytest
from appointments.models import Seat
from ..prices import calculate_price, PaymentMethodType


class TestCalculatePayments:
    def test_calculate_only_has_doctor_referral(self):
        s1 = Seat(has_doctor_referral=True)
        s2 = Seat(has_doctor_referral=True)
        res = calculate_price([s1, s2], PaymentMethodType.ON_SITE)
        assert res == {
            "total_price": 0,
            "currency": "HUF",
        }

    def test_calculate_ON_SITE_only(self):
        s1 = Seat()
        s2 = Seat()
        res = calculate_price([s1, s2], PaymentMethodType.ON_SITE)
        assert res == {
            "total_price": 24_000,
            "currency": "HUF",
        }

    def test_calculate_has_doctor_referral_and_ON_SITE(self):
        s1 = Seat(has_doctor_referral=True)
        s2 = Seat()
        res = calculate_price([s1, s2], PaymentMethodType.ON_SITE)
        assert res == {
            "total_price": 12_000,
            "currency": "HUF",
        }

    def test_calculate_has_doctor_referral_and_2_ON_SITE(self):
        s1 = Seat(has_doctor_referral=True)
        s2 = Seat()
        s3 = Seat()
        res = calculate_price([s1, s2, s3], PaymentMethodType.ON_SITE)
        assert res == {
            "total_price": 24_000,
            "currency": "HUF",
        }

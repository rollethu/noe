import datetime as dt
from ..models import PhoneVerification


def test_phone_is_verified():
    pv = PhoneVerification()
    assert pv.is_verified is False

    pv.verified_at = dt.datetime.now()
    assert pv.is_verified is True

import datetime as dt
import pytest
from .. import models as m


def test_phone_is_verified():
    pv = m.PhoneVerification()
    assert pv.is_verified is False

    pv.verified_at = dt.datetime.now()
    assert pv.is_verified is True


def test_email_is_verified():
    ev = m.EmailVerification()
    assert ev.is_verified is False

    ev.verified_at = dt.datetime.now()
    assert ev.is_verified is True


@pytest.mark.django_db
def test_verify_token():
    email = "user@rollet.app"
    appointment = m.Appointment(gtc="1.0", privacy_policy="1.0", email=email)
    appointment.save()
    ev = m.EmailVerification(appointment=appointment)
    ev.save()
    token = ev.make_token()

    # Just to make sure there are multiple verifications and we select the good one
    for _ in range(10):
        new_ev = m.EmailVerification(appointment=appointment)
        new_ev.save()

    expected_ev, signed_uuid = m.EmailVerification.objects.get_by_token(token)
    assert ev.uuid == expected_ev.uuid

    expected_ev.verify(signed_uuid)
    assert expected_ev.is_verified is True

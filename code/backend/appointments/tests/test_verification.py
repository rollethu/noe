import datetime as dt
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


def test_sign_email_verification():
    email = "user@rollet.app"
    appointment = m.Appointment(gtc="1.0", privacy_policy="1.0", email=email)
    ev = m.EmailVerification(appointment=appointment)
    signed_email = ev.sign()
    print("SIGNED EMAIL:", signed_email)
    assert signed_email.startswith(email + ":")
    assert ev.verify(signed_email) is True

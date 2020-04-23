import datetime as dt
from urllib.parse import quote
from django.core import mail
from django.conf import settings
import pytest
from .. import email
from .. import models as m


def test_send_verification():
    address = "test@rollet.app"
    ev = m.EmailVerification()
    token = ev.make_token()

    email.send_verification(token, address)

    assert len(mail.outbox) == 1

    sent_mail = mail.outbox[0]

    assert sent_mail.to == [address]
    assert "erősítse meg" in sent_mail.body
    assert settings.FRONTEND_URL in sent_mail.body
    assert quote(token) in sent_mail.body


@pytest.mark.django_db
def test_send_summary(appointment, location, seat, qr):
    appointment.start = dt.datetime(2020, 4, 24, 9, 10)

    email.send_summary(appointment, qr.make_png(), "test@rollet.app")
    assert len(mail.outbox) == 1

    sent_mail = mail.outbox[0]
    print(sent_mail.body)
    assert appointment.normalized_licence_plate in sent_mail.body
    assert location.name in sent_mail.body


@pytest.mark.django_db
def test_send_summary_doctor_referral(appointment, seat, qr):
    seat.has_doctor_referral = True
    seat.save()
    appointment.seats.add(seat)
    email.send_summary(appointment, qr.make_png(), "test@rollet.app")
    sent_mail = mail.outbox[0]
    assert "Orvosi beutalóval érkezik" in sent_mail.body

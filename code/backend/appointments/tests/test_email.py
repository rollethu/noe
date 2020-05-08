import datetime as dt
from urllib.parse import quote
from django.core import mail
from django.conf import settings
from django.utils import timezone
import pytest
from payments.models import Payment
from payments.prices import PaymentMethodType, ProductType
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


def test_send_qrcode():
    code = "0123-123456-1111"
    licence_plate = "ABC123"
    location_name = "Test Location"
    full_name = "Gipsz Jakab"

    location = m.Location(name=location_name)
    appointment = m.Appointment(
        start=dt.datetime(2020, 4, 24, 9, 10), location=location, normalized_licence_plate=licence_plate
    )
    payment = Payment(
        amount=26_990, payment_method_type=PaymentMethodType.ON_SITE, product_type=ProductType.NORMAL_EXAM,
    )
    seat = m.Seat(
        full_name=full_name,
        birth_date=timezone.now(),
        email="test@rollet.app",
        appointment=appointment,
        qrcode=m.QRCode(code=code),
        payment=payment,
    )

    email.send_qrcode(seat)
    assert len(mail.outbox) == 1

    sent_mail = mail.outbox[0]
    assert full_name in sent_mail.body
    assert licence_plate in sent_mail.body
    assert location.name in sent_mail.body
    assert "Helyszínen" in sent_mail.body
    assert "Test Location" in sent_mail.body
    assert code in sent_mail.body
    assert "\nFizetendő összeg: 26990 Ft\n" in sent_mail.body
    assert "\nVizsgálat típusa: Normál vizsgálat\n" in sent_mail.body
    assert "A normál vizsgálatok eredményét 72 órán belül küldjük Önnek." in sent_mail.body


def test_send_qrcode_with_priority_product():
    location = m.Location(name="Test Location")
    appointment = m.Appointment(
        start=dt.datetime(2020, 4, 24, 9, 10), location=location, normalized_licence_plate="ABC123"
    )
    payment = Payment(
        amount=36_990, payment_method_type=PaymentMethodType.ON_SITE, product_type=ProductType.PRIORITY_EXAM,
    )
    seat = m.Seat(
        full_name="Gipsz Jakab",
        birth_date=timezone.now(),
        email="test@rollet.app",
        appointment=appointment,
        qrcode=m.QRCode(code="0123-123456-1111"),
        payment=payment,
    )

    email.send_qrcode(seat)
    assert len(mail.outbox) == 1

    sent_mail = mail.outbox[0]
    assert "\nFizetendő összeg: 36990 Ft\n" in sent_mail.body
    assert "\nVizsgálat típusa: Elsőbbségi vizsgálat\n" in sent_mail.body
    assert "Az elsőbbségi vizsgálatok eredményét a teszt elvégzését követő napon küldjük Önnek." in sent_mail.body


def test_send_qrcode_with_doctor_referral():
    seat = m.Seat(
        has_doctor_referral=True,
        birth_date=timezone.now(),
        email="test@rollet.app",
        appointment=m.Appointment(),
        qrcode=m.QRCode(),
        payment=Payment(amount=0),
    )

    email.send_qrcode(seat)
    sent_mail = mail.outbox[0]
    assert "orvosi beutalót" in sent_mail.body

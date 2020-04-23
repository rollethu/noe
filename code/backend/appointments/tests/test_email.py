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

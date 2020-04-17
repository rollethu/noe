from django.core import mail
import pytest
from .. import views
from .. import models as m


@pytest.fixture
def email_verification():
    appointment = m.Appointment.objects.create(gtc="1.0", privacy_policy="1.0", email="info@tesztallomas.hu")
    ev = appointment.email_verifications.first()
    return ev


def test_email_verify_with_invalid_token(factory):
    request = factory.post("/email/verify/", {"token": "invalid-token"})
    view = views.VerifyEmailView.as_view()
    response = view(request)
    assert response.status_code == 400


@pytest.mark.django_db
def test_email_verify_with_valid_token(factory, email_verification):
    assert email_verification.is_verified is False

    request = factory.post("/verify/email/", {"token": email_verification.make_token()})

    view = views.VerifyEmailView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert "appointment_url" in response.data
    assert "appointment_email" in response.data

    email_verification.refresh_from_db()
    assert email_verification.is_verified is True


@pytest.mark.django_db
def test_resend_email_verification_sends_email(factory, email_verification):
    view = views.ResendVerifyEmailView.as_view()

    request = factory.post("/verify/resend-email/", {"uuid": email_verification.uuid})
    assert len(mail.outbox) == 0
    response = view(request)
    assert len(mail.outbox) == 1
    assert response.data["email"] == email_verification.appointment.email

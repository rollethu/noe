from rest_framework.test import APIRequestFactory
import pytest
from .. import views
from .. import models as m


def test_email_verify_with_invalid_token():
    factory = APIRequestFactory()
    request = factory.post("/email/verify/", {"token": "invalid-token"})
    view = views.VerifyEmailView.as_view()
    response = view(request)
    assert response.status_code == 400


@pytest.mark.django_db
def test_email_verify_with_valid_token():
    appointment = m.Appointment.objects.create(gtc="1.0", privacy_policy="1.0", email="info@tesztallomas.hu")
    ev = appointment.email_verifications.first()
    assert ev.is_verified is False

    factory = APIRequestFactory()
    request = factory.post("/email/verify/", {"token": ev.make_token()})

    view = views.VerifyEmailView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert "appointment_url" in response.data
    assert "appointment_email" in response.data

    ev.refresh_from_db()
    assert ev.is_verified is True

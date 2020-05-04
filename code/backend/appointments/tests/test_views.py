from django.core import mail
from django.conf import settings
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APIClient
import pytest
from payments.models import Payment
from .. import views
from .. import models as m


@pytest.fixture
def email_verification():
    appointment = m.Appointment.objects.create(gtc="1.0", privacy_policy="1.0", email="info@tesztallomas.hu")
    ev = appointment.email_verifications.first()
    return ev


@pytest.fixture
def staff_api_browser(api_user, api_client):
    # We simulate the user coming from the browser with Session authentication
    api_client.force_authenticate(user=api_user, token=None)
    return api_client


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
def test_appointment_creation_sends_email(api_client):
    assert len(mail.outbox) == 0
    response = api_client.post(
        "/api/appointments/", {"email": "test@rollet.app", "gtc": "1.0", "privacy_policy": "1.0"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_resend_email_verification_sends_email(factory, email_verification):
    view = views.ResendVerifyEmailView.as_view()

    request = factory.post("/verify/resend-email/", {"uuid": email_verification.uuid})
    assert len(mail.outbox) == 0
    response = view(request)
    assert len(mail.outbox) == 1
    assert response.data["email"] == email_verification.appointment.email


@pytest.mark.django_db
class TestQRCodeView:
    def test_redirect_to_admin(self, staff_api_browser, api_user, seat, qr):
        rv = staff_api_browser.get(qr.get_absolute_url())
        assert rv.status_code == status.HTTP_302_FOUND
        assert rv["location"] == reverse("admin:appointments_seat_change", kwargs={"object_id": seat.pk})

    def test_redirect_to_seat_detail_when_using_browsable_api(self, staff_api_browser, api_user, seat, qr):
        http_get_params = {"format": "api"}
        rv = staff_api_browser.get(qr.get_absolute_url(), http_get_params)
        assert rv.status_code == status.HTTP_302_FOUND

        seat_url = reverse("staff-seat-detail", kwargs={"pk": seat.pk})
        assert rv["location"] == f"{seat_url}?format=api"

    def test_redirect_to_seat_detail_when_using_json_format(self, staff_api_browser, api_user, seat, qr):
        http_get_params = {"format": "json"}
        rv = staff_api_browser.get(qr.get_absolute_url(), http_get_params)
        assert rv.status_code == status.HTTP_302_FOUND

        seat_url = reverse("staff-seat-detail", kwargs={"pk": seat.pk})
        assert rv["location"] == f"{seat_url}?format=json"

    def test_redirect_to_seat_detail_when_using_token_auth(self, staff_api_client, seat, qr):
        rv = staff_api_client.get(qr.get_absolute_url())
        assert rv.status_code == status.HTTP_302_FOUND

        seat_url = reverse("staff-seat-detail", kwargs={"pk": seat.pk})
        assert rv["location"] == seat_url

    def test_return_404_when_qrcode_has_no_Seat(self, staff_api_client):
        qr_noseat = m.QRCode.objects.create()
        rv = staff_api_client.get(qr_noseat.get_absolute_url())
        assert rv.status_code == status.HTTP_404_NOT_FOUND

    def test_redirect_to_frontend_when_not_logged_in(self, api_client, qr):
        rv = api_client.get(qr.get_absolute_url())
        assert rv.status_code == status.HTTP_302_FOUND
        assert rv["location"] == settings.FRONTEND_URL

    def test_redirect_to_frontend_when_not_logged_in_even_without_seat(self, api_client):
        qr_noseat = m.QRCode.objects.create()
        rv = api_client.get(qr_noseat.get_absolute_url())
        assert rv.status_code == status.HTTP_302_FOUND
        assert rv["location"] == settings.FRONTEND_URL


@pytest.mark.django_db
class TestRegistrationCompleted:
    def test_seat_with_empty_email_raises_ValidationError(self, appointment, seat, appointment_client):
        appointment.seats.add(seat)

        appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
        res = appointment_client.patch(appointment_url, {"is_registration_completed": True})
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert len(mail.outbox) == 0
        assert m.QRCode.objects.count() == 0

        appointment.refresh_from_db()
        assert appointment.is_registration_completed is False

    def test_one_seat(self, appointment, appointment_client):
        seat = m.Seat.objects.create(birth_date=timezone.now(), email="test@rollet.app", appointment=appointment)
        Payment.objects.create(amount=100, seat=seat)
        appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
        res = appointment_client.patch(appointment_url, {"is_registration_completed": True})
        assert res.status_code == status.HTTP_200_OK
        assert m.QRCode.objects.count() == 1

        appointment.refresh_from_db()
        assert appointment.is_registration_completed is True
        assert len(mail.outbox) == 1

    def test_multiple_seats_same_email(self, appointment, appointment_client):
        same_email = "test@rollet.app"
        seat1 = m.Seat.objects.create(birth_date=timezone.now(), email=same_email, appointment=appointment)
        Payment.objects.create(amount=100, seat=seat1)
        seat2 = m.Seat.objects.create(birth_date=timezone.now(), email=same_email, appointment=appointment)
        Payment.objects.create(amount=100, seat=seat2)

        appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
        res = appointment_client.patch(appointment_url, {"is_registration_completed": True})
        assert res.status_code == status.HTTP_200_OK
        assert m.QRCode.objects.count() == 2

        appointment.refresh_from_db()
        assert appointment.is_registration_completed is True
        assert len(mail.outbox) == 2

    def test_multiple_seats_different_emails(self, appointment, appointment_client):
        seat1 = m.Seat.objects.create(birth_date=timezone.now(), email="test1@rollet.app", appointment=appointment)
        Payment.objects.create(amount=100, seat=seat1)
        seat2 = m.Seat.objects.create(birth_date=timezone.now(), email="test2@rollet.app", appointment=appointment)
        Payment.objects.create(amount=100, seat=seat2)
        seat3 = m.Seat.objects.create(birth_date=timezone.now(), email="test3@rollet.app", appointment=appointment)
        Payment.objects.create(amount=100, seat=seat3)

        appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
        res = appointment_client.patch(appointment_url, {"is_registration_completed": True})
        assert res.status_code == status.HTTP_200_OK
        assert m.QRCode.objects.count() == 3

        appointment.refresh_from_db()
        assert appointment.is_registration_completed is True
        assert len(mail.outbox) == 3

    def test_proper_qrcode_format(self, appointment, appointment_client):
        seat = m.Seat.objects.create(birth_date=timezone.now(), email="test@rollet.app", appointment=appointment)
        Payment.objects.create(amount=100, seat=seat)

        appointment_url = reverse("appointment-detail", kwargs={"pk": appointment.pk})
        res = appointment_client.patch(appointment_url, {"is_registration_completed": True})
        assert res.status_code == status.HTTP_200_OK
        assert m.QRCode.objects.count() == 1

        qr = m.QRCode.objects.get()
        assert qr.code == qr._calc_code()

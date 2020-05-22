from unittest.mock import Mock

from django.core import mail
from django.utils import timezone
from django.db.models import Sum
from online_payments.payments.simple_v2.client import IPN, StartPaymentResponse
from online_payments.payments.simple_v2.exceptions import IPNError
from online_payments.payments.exceptions import InvalidSignature
from rest_framework.test import force_authenticate
from rest_framework import status
import pytest

from appointments.models import Seat, EmailVerification, QRCode
from ..views import (
    GetPriceView,
    PayAppointmentView,
    PaymentStatusView,
    simplepay_v2_callback_view as callback_view,
    simplepay,
)
from billing import services as billing_services
from feature_flags import use_feature_simplepay
from ..prices import ProductType, PaymentMethodType
from .. import models as m

get_price_view = GetPriceView.as_view()
pay_appointment_view = PayAppointmentView.as_view()
payment_status_view = PaymentStatusView.as_view()


@pytest.fixture
def get_price_request(factory, appointment, appointment_url):
    request = factory.post(
        "/api/get-price/", {"appointment": appointment_url, "product_type": ProductType.NORMAL_EXAM}
    )
    _authenticate_appointment(request, appointment)
    return request


# This is mutated inside tests, so we need a new instance for every test
@pytest.fixture(scope="function")
def pay_appointment_body(appointment_url):
    return {
        "appointment": appointment_url,
        "product_type": ProductType.NORMAL_EXAM,
        "payment_method": PaymentMethodType.ON_SITE,
        "total_price": 0,
        "currency": "HUF",
        "company_name": "Test Company",
        "country": "Magyarország",
        "address_line1": "Test Address Line 1",
        "post_code": "1234",
        "city": "Budapest",
        "tax_number": "123456789",
    }


def _authenticate_appointment(request, appointment):
    ev = EmailVerification.objects.create(appointment=appointment)
    force_authenticate(request, token=appointment)


def _assert_payments(count, expected_total_price):
    assert m.Payment.objects.count() == count
    aggres = m.Payment.objects.aggregate(total_price=Sum("amount"))
    assert aggres["total_price"] == expected_total_price


@pytest.mark.django_db
class TestGetPriceView:
    def test_appointment_with_no_seats(self, appointment_url, get_price_request, factory):
        res = get_price_view(get_price_request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == 0
        _assert_payments(count=0, expected_total_price=None)

    def test_appointment_with_one_seat(self, get_price_request, seat):
        res = get_price_view(get_price_request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == 24_980
        _assert_payments(count=0, expected_total_price=None)

    def test_appointment_with_multiple_seats(self, get_price_request, appointment):
        Seat.objects.create(appointment=appointment, birth_date=timezone.now())
        Seat.objects.create(appointment=appointment, birth_date=timezone.now())
        res = get_price_view(get_price_request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == 24_980 * 2
        _assert_payments(count=0, expected_total_price=None)

    def test_appointment_seat_with_has_doctor_referral(self, get_price_request, appointment):
        Seat.objects.create(appointment=appointment, birth_date=timezone.now(), has_doctor_referral=True)
        res = get_price_view(get_price_request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == 0
        _assert_payments(count=0, expected_total_price=None)

    def test_appointment_multiple_seats_with_has_doctor_referral(self, get_price_request, appointment):
        Seat.objects.create(appointment=appointment, birth_date=timezone.now(), has_doctor_referral=True)
        Seat.objects.create(appointment=appointment, birth_date=timezone.now())
        Seat.objects.create(appointment=appointment, birth_date=timezone.now())
        res = get_price_view(get_price_request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == 24_980 * 2
        _assert_payments(count=0, expected_total_price=None)

    def test_completed_registration(self, get_price_request, appointment):
        appointment.is_registration_completed = True
        appointment.save()
        res = get_price_view(get_price_request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        _assert_payments(count=0, expected_total_price=None)


@pytest.mark.django_db
class TestPayAppointmentView:
    def test_cannot_pay_zero_seats(self, appointment, pay_appointment_body, factory):
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "appointment" in res.data
        _assert_payments(count=0, expected_total_price=None)

    def test_seat_with_empty_email_raises_ValidationError(self, pay_appointment_body, seat, factory, appointment):
        seat.email = ""
        seat.save()
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST

    def test_pay_one_seat(self, pay_appointment_body, seat, factory, appointment):
        appointment.email = "test@rollet.app"
        total_price = 24_980
        pay_appointment_body["total_price"] = total_price
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == total_price
        _assert_payments(count=1, expected_total_price=total_price)

        appointment.refresh_from_db()
        assert appointment.is_registration_completed is True
        assert QRCode.objects.count() == 1
        assert len(mail.outbox) == 1

    @pytest.mark.vcr()
    @pytest.mark.skipif(not use_feature_simplepay, reason="SimplePay feature is turned off")
    def test_simplepay(self, pay_appointment_body, seat, factory, appointment):
        total_price = 24_980
        pay_appointment_body["total_price"] = total_price
        pay_appointment_body["payment_method"] = PaymentMethodType.SIMPLEPAY
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK
        _assert_payments(count=1, expected_total_price=total_price)

        appointment.refresh_from_db()
        assert appointment.is_registration_completed is False
        assert QRCode.objects.count() == 0
        assert len(mail.outbox) == 0
        assert m.SimplePayTransaction.objects.exists()
        transaction = m.SimplePayTransaction.objects.first()
        assert transaction.external_reference_id
        assert transaction in seat.payment.simplepay_transactions.all()
        assert transaction.status == transaction.STATUS_WAITING_FOR_AUTHORIZATION

    def test_pay_multiple_seats_different_email(self, appointment, pay_appointment_body, factory):
        Seat.objects.create(appointment=appointment, birth_date=timezone.now(), email="seat@email.com")
        Seat.objects.create(appointment=appointment, birth_date=timezone.now(), email="seat2@email.com")

        total_price = 24_980 * 2
        pay_appointment_body["total_price"] = total_price

        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == total_price
        _assert_payments(count=2, expected_total_price=total_price)
        assert QRCode.objects.count() == 2
        assert len(mail.outbox) == 2

        appointment.refresh_from_db()
        assert appointment.is_registration_completed is True

    def test_pay_multiple_seats_same_email(self, appointment, pay_appointment_body, factory):
        same_email = "test@rollet.app"
        Seat.objects.create(appointment=appointment, birth_date=timezone.now(), email=same_email)
        Seat.objects.create(appointment=appointment, birth_date=timezone.now(), email=same_email)

        total_price = 24_980 * 2
        pay_appointment_body["total_price"] = total_price
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == total_price
        _assert_payments(count=2, expected_total_price=total_price)
        assert QRCode.objects.count() == 2
        assert len(mail.outbox) == 2

        appointment.refresh_from_db()
        assert appointment.is_registration_completed is True

    def test_pay_multiple_seats_doctor_referral_only(self, appointment, pay_appointment_body, factory):
        Seat.objects.create(
            appointment=appointment, birth_date=timezone.now(), has_doctor_referral=True, email="seat@email.com"
        )
        Seat.objects.create(
            appointment=appointment, birth_date=timezone.now(), has_doctor_referral=True, email="seat@email.com"
        )

        total_price = 0
        pay_appointment_body["total_price"] = total_price
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == total_price
        _assert_payments(count=2, expected_total_price=total_price)

    def test_cannot_pay_completed_registration(self, appointment, pay_appointment_body, seat, factory):
        appointment.is_registration_completed = True
        appointment.save()

        pay_appointment_body["total_price"] = 0

        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "appointment" in res.data
        _assert_payments(count=0, expected_total_price=None)

    def test_different_total_price_sent_than_calculated(self, appointment, pay_appointment_body, seat, factory):
        pay_appointment_body["total_price"] = 0
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "total_price" in res.data
        _assert_payments(count=0, expected_total_price=None)

    def test_proper_qrcode_format(self, pay_appointment_body, seat, factory, appointment):
        pay_appointment_body["total_price"] = 24_980
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK
        assert QRCode.objects.count() == 1

        qr = QRCode.objects.get()
        assert qr.code == qr._calc_code()

    def test_tax_number_is_optional_if_not_company(self, pay_appointment_body, factory, appointment, seat):
        pay_appointment_body["total_price"] = 24_980
        pay_appointment_body.pop("tax_number", None)
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK, res.data

    def test_tax_number_is_optional_if_not_company2(self, pay_appointment_body, factory, appointment, seat):
        pay_appointment_body["total_price"] = 24_980
        pay_appointment_body["tax_number"] = ""
        request = factory.post("/api/pay-appointment/", pay_appointment_body, format="json")
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK, res.data

    def test_tax_number_is_required_if_company(self, pay_appointment_body, factory, appointment, seat):
        pay_appointment_body["total_price"] = 24_980
        pay_appointment_body.pop("tax_number", None)
        pay_appointment_body["is_company"] = True
        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "tax_number" in res.data

    @pytest.mark.skipif(not use_feature_simplepay, reason="SimplePay feature is turned off")
    def test_existing_payments(self, pay_appointment_body, factory, transaction, appointment, monkeypatch):
        mock_response = Mock(
            return_value=StartPaymentResponse(
                salt="12345",
                merchant="12345",
                order_ref="12345",
                currency="12345",
                transaction_id="2222",
                timeout=timezone.now(),
                total="12345",
                payment_url="12345",
            )
        )
        monkeypatch.setattr(simplepay, "start", mock_response)

        pay_appointment_body["total_price"] = 24_980
        pay_appointment_body["payment_method"] = PaymentMethodType.SIMPLEPAY

        request = factory.post("/api/pay-appointment/", pay_appointment_body)
        _authenticate_appointment(request, appointment)
        res = pay_appointment_view(request)

        assert res.status_code == status.HTTP_200_OK
        assert m.SimplePayTransaction.objects.count() == 2

        new_transaction = m.SimplePayTransaction.objects.order_by("created_at").last()
        assert new_transaction.external_reference_id == "2222"
        assert set(new_transaction.payments.all()) == set(transaction.payments.all())


class TestPaymentStatusView:
    def test_without_auth(self, factory):
        request = factory.get("/fake-url")
        rv = payment_status_view(request)
        assert rv.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_with_auth_without_resources(self, factory, appointment):
        request = factory.get("/fake-url")
        _authenticate_appointment(request, appointment)
        rv = payment_status_view(request)
        assert rv.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.mark.django_db
    def test_pending(self, factory, appointment, seat, payment, transaction):
        transaction.status = transaction.STATUS_WAITING_FOR_AUTHORIZATION
        transaction.save()

        request = factory.get("/fake-url")
        _authenticate_appointment(request, appointment)
        rv = payment_status_view(request)
        assert rv.status_code == status.HTTP_200_OK
        assert rv.data["payment_status"] == "PENDING"

    @pytest.mark.django_db
    def test_finds_correct_transaction(self, factory, appointment, seat, payment, transaction, transaction2):
        transaction2.status = transaction.STATUS_COMPLETED
        transaction2.save()

        request = factory.get("/fake-url")
        _authenticate_appointment(request, appointment)
        rv = payment_status_view(request)
        assert rv.status_code == status.HTTP_200_OK
        assert rv.data["payment_status"] == "SUCCESS"


@pytest.mark.skipif(not use_feature_simplepay, reason="SimplePay feature is turned off")
class TestSimplePayCallbackView:
    url = "/simplepay-callback/"

    @pytest.mark.django_db
    def test_success(self, factory, monkeypatch, transaction, api_client, appointment_billing_detail):
        mock_send_appointment_invoice = Mock()
        monkeypatch.setattr(billing_services, "send_appointment_invoice", mock_send_appointment_invoice)
        now = timezone.now()

        transaction.external_reference_id = "111"
        transaction.save()

        mockIPN = IPN(
            transaction_id="111",
            salt="salt",
            order_ref="order_ref",
            method="method",
            merchant="merchant",
            finish_date=now,
            payment_date="123",
            status="FINISHED",
        )
        mockResponse = {"body": "", "headers": {}}
        monkeypatch.setattr(simplepay, "process_ipn_request", Mock(return_value=(mockIPN, mockResponse)))
        rv = api_client.post(self.url)
        assert rv.status_code == status.HTTP_200_OK
        transaction.refresh_from_db()
        assert transaction.status == transaction.STATUS_COMPLETED
        assert transaction.payments.order_by("created_at").last().paid_at == now
        mock_send_appointment_invoice.assert_called()

    def test_ipn_error_is_handled(self, api_client, monkeypatch):
        mock_ipn_process = Mock(side_effect=(IPNError()))
        monkeypatch.setattr(simplepay, "process_ipn_request", mock_ipn_process)
        rv = api_client.post(self.url)
        assert rv.status_code == status.HTTP_400_BAD_REQUEST

    def test_invalid_signature_is_handled(self, api_client, monkeypatch):
        mock_ipn_process = Mock(side_effect=(InvalidSignature()))
        monkeypatch.setattr(simplepay, "process_ipn_request", mock_ipn_process)
        rv = api_client.post(self.url)
        assert rv.status_code == status.HTTP_400_BAD_REQUEST

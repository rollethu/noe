from django.utils import timezone
from django.db.models import Sum
from rest_framework.reverse import reverse
from rest_framework import status
import pytest
from appointments.models import Seat
from ..views import GetPriceView, PayAppointmentView
from ..prices import ProductType
from .. import models as m

get_price_view = GetPriceView.as_view()
pay_appointment_view = PayAppointmentView.as_view()


@pytest.fixture
def appointment_url(appointment):
    appointment_path = reverse("appointment-detail", args=[appointment.uuid])
    return "http://localhost" + appointment_path


@pytest.fixture
def get_price_request(factory, appointment_url):
    return factory.post("/api/get-price/", {"appointment": appointment_url, "product_type": ProductType.NORMAL_EXAM})


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
        assert res.data["total_price"] == 26_990
        _assert_payments(count=0, expected_total_price=None)

    def test_appointment_with_multiple_seats(self, get_price_request, appointment):
        Seat.objects.create(appointment=appointment, birth_date=timezone.now())
        Seat.objects.create(appointment=appointment, birth_date=timezone.now())
        res = get_price_view(get_price_request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == 26_990 * 2
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
        assert res.data["total_price"] == 26_990 * 2
        _assert_payments(count=0, expected_total_price=None)

    def test_completed_registration(self, get_price_request, appointment):
        appointment.is_registration_completed = True
        appointment.save()
        res = get_price_view(get_price_request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        _assert_payments(count=0, expected_total_price=None)


@pytest.mark.django_db
class TestPayAppointmentView:
    def test_cannot_pay_zero_seats(self, appointment_url, factory):
        request = factory.post(
            "/api/pay-appointment/",
            {
                "appointment": appointment_url,
                "product_type": ProductType.NORMAL_EXAM,
                "total_price": 0,
                "currency": "HUF",
            },
        )
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "appointment" in res.data
        _assert_payments(count=0, expected_total_price=None)

    def test_pay_one_seat(self, appointment_url, seat, factory):
        total_price = 26_990
        request = factory.post(
            "/api/pay-appointment/",
            {
                "appointment": appointment_url,
                "product_type": ProductType.NORMAL_EXAM,
                "total_price": total_price,
                "currency": "HUF",
            },
        )
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == total_price
        _assert_payments(count=1, expected_total_price=total_price)

    def test_pay_multiple_seats(self, appointment, appointment_url, factory):
        Seat.objects.create(appointment=appointment, birth_date=timezone.now())
        Seat.objects.create(appointment=appointment, birth_date=timezone.now())

        total_price = 26_990 * 2
        request = factory.post(
            "/api/pay-appointment/",
            {
                "appointment": appointment_url,
                "product_type": ProductType.NORMAL_EXAM,
                "total_price": total_price,
                "currency": "HUF",
            },
        )
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == total_price
        _assert_payments(count=2, expected_total_price=total_price)

    def test_pay_multiple_seats_doctor_referral_only(self, appointment, appointment_url, factory):
        Seat.objects.create(appointment=appointment, birth_date=timezone.now(), has_doctor_referral=True)
        Seat.objects.create(appointment=appointment, birth_date=timezone.now(), has_doctor_referral=True)

        total_price = 0
        request = factory.post(
            "/api/pay-appointment/",
            {
                "appointment": appointment_url,
                "product_type": ProductType.NORMAL_EXAM,
                "total_price": total_price,
                "currency": "HUF",
            },
        )
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_200_OK
        assert res.data["total_price"] == total_price
        _assert_payments(count=2, expected_total_price=total_price)

    def test_cannot_pay_completed_registration(self, appointment, appointment_url, seat, factory):
        appointment.is_registration_completed = True
        appointment.save()

        request = factory.post(
            "/api/pay-appointment/",
            {
                "appointment": appointment_url,
                "product_type": ProductType.NORMAL_EXAM,
                "total_price": 0,
                "currency": "HUF",
            },
        )
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "appointment" in res.data
        _assert_payments(count=0, expected_total_price=None)

    def test_different_total_price_sent_than_calculated(self, appointment_url, seat, factory):
        request = factory.post(
            "/api/pay-appointment/",
            {
                "appointment": appointment_url,
                "product_type": ProductType.NORMAL_EXAM,
                "total_price": 0,
                "currency": "HUF",
            },
        )
        res = pay_appointment_view(request)
        assert res.status_code == status.HTTP_400_BAD_REQUEST
        assert "total_price" in res.data
        _assert_payments(count=0, expected_total_price=None)

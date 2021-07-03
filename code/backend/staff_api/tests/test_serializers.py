import datetime as dt

import pytest
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from rest_framework.test import force_authenticate

from appointments.models import Seat
from payments.models import Payment
from .. import serializers as s


@pytest.mark.django_db
class TestAppointmentSerializer:
    def test_seat_with_0_amount_not_paid(self, appointment):
        ser = s.AppointmentSerializer()
        seat = Seat(appointment=appointment, birth_date=timezone.now())
        seat.save()
        payment = Payment(amount=0, seat=seat)
        payment.save()
        assert ser.get_all_seats_paid(appointment) is False

    def test_seat_with_0_amount_paid(self, appointment):
        ser = s.AppointmentSerializer()
        seat = Seat(appointment=appointment, birth_date=timezone.now())
        seat.save()
        payment = Payment(amount=0, seat=seat, paid_at=timezone.now())
        payment.save()
        assert ser.get_all_seats_paid(appointment) is True

    def test_two_seats_one_paid(self, appointment):
        ser = s.AppointmentSerializer()

        seat1 = Seat(appointment=appointment, birth_date=timezone.now())
        seat1.save()
        payment1 = Payment(amount=100, seat=seat1, paid_at=timezone.now())
        payment1.save()

        seat2 = Seat(appointment=appointment, birth_date=timezone.now())
        seat2.save()
        payment2 = Payment(amount=100, seat=seat2)
        payment2.save()

        assert ser.get_all_seats_paid(appointment) is False

    def test_two_seats_all_paid(self, appointment):
        ser = s.AppointmentSerializer()

        seat1 = Seat(appointment=appointment, birth_date=timezone.now())
        seat1.save()
        payment1 = Payment(amount=200, seat=seat1, paid_at=timezone.now())
        payment1.save()

        seat2 = Seat(appointment=appointment, birth_date=timezone.now())
        seat2.save()
        payment2 = Payment(amount=200, seat=seat2, paid_at=timezone.now())
        payment2.save()

        assert ser.get_all_seats_paid(appointment) is True


@pytest.mark.django_db
class TestPaymentSerializer:
    def test_no_paid_at_in_data(self, payment, send_seat_invoice_mock):
        ser = s.PaymentSerializer(payment, {}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        send_seat_invoice_mock.assert_not_called()

    def test_explicit_none_in_data(self, payment, send_seat_invoice_mock):
        ser = s.PaymentSerializer(payment, {"paid_at": None}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()
        send_seat_invoice_mock.assert_not_called()

    def test_explicit_none_but_already_set(self, payment):
        payment.paid_at = timezone.now()
        payment.save()

        ser = s.PaymentSerializer(payment, {"paid_at": None}, partial=True)
        ser.is_valid(raise_exception=True)
        with pytest.raises(ValidationError):
            ser.save()

    def test_setting_value(self, seat, payment, send_seat_invoice_mock):
        ser = s.PaymentSerializer(payment, {"paid_at": timezone.now()}, partial=True)
        ser.is_valid(raise_exception=True)
        ser.save()

        assert payment.seat == seat
        send_seat_invoice_mock.assert_called_with(seat)

    def test_resetting_value_raises(self, seat, payment):
        payment.paid_at = timezone.now()
        payment.save()

        ser = s.PaymentSerializer(payment, {"paid_at": timezone.now()}, partial=True)
        ser.is_valid(raise_exception=True)
        with pytest.raises(ValidationError):
            ser.save()


@pytest.mark.django_db
class TestSeatSerializer:
    def test_location_name_is_included(self, seat, location, factory, api_user):
        appointment = seat.appointment
        appointment.location = location
        appointment.save()

        request = factory.get("fake-url")
        request.user = api_user
        serializer = s.SeatSerializer(seat, context={"request": request})
        assert serializer.data["location_name"] == location.name

    def test_is_correct_location(self, seat, factory, api_user):
        appointment = seat.appointment

        request = factory.get("fake-url")
        request.user = api_user
        serializer = s.SeatSerializer(seat, context={"request": request})
        assert serializer.data["is_correct_location"] is False

        appointment.location = api_user.location
        appointment.save()
        serializer = s.SeatSerializer(seat, context={"request": request})
        assert serializer.data["is_correct_location"] is True

    def test_is_appointment_expired(self, seat, factory, api_user):
        request = factory.get("fake-url")
        request.user = api_user
        appointment = seat.appointment

        appointment.end = None
        appointment.save()
        serializer = s.SeatSerializer(seat, context={"request": request})
        assert serializer.data["is_appointment_expired"] is False

        appointment.end = timezone.now()
        appointment.save()
        serializer = s.SeatSerializer(seat, context={"request": request})
        assert serializer.data["is_appointment_expired"] is False

        appointment.end = timezone.now() + dt.timedelta(days=1)
        appointment.save()
        serializer = s.SeatSerializer(seat, context={"request": request})
        assert serializer.data["is_appointment_expired"] is False

        appointment.end = timezone.now() - dt.timedelta(days=1)
        appointment.save()
        serializer = s.SeatSerializer(seat, context={"request": request})
        assert serializer.data["is_appointment_expired"] is True

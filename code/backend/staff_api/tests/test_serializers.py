import pytest
from django.utils import timezone
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

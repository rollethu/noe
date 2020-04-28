import datetime as dt

import pytz
import pytest
from django.utils.timezone import make_aware as maw, make_naive
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse

from appointments import models as m


def test_create_one_time_slot(location_no_db):
    time_slot_duration = dt.timedelta(minutes=30)
    time_slot_generation_duration = dt.timedelta(minutes=15)
    assert time_slot_duration > time_slot_generation_duration

    now = timezone.now()
    start = now
    end = now + time_slot_generation_duration
    is_active = True
    capacity = 100
    time_slots = m.TimeSlot.objects._make_time_slots(
        [location_no_db], start, end, time_slot_duration, is_active, capacity
    )

    assert len(time_slots) == 1
    time_slot = time_slots[0]
    assert time_slot.location == location_no_db
    assert time_slot.start == now
    assert time_slot.end == start + time_slot_duration
    assert time_slot.is_active
    assert time_slot.capacity == 100


@pytest.mark.parametrize(
    "location_count, start, end, expected_count",
    [
        (1, dt.datetime(2020, 1, 1, 12), dt.datetime(2020, 1, 1, 12, 1), 1),
        (1, dt.datetime(2020, 1, 1, 12), dt.datetime(2020, 1, 1, 14), 4),
        (3, dt.datetime(2020, 1, 1, 12), dt.datetime(2020, 1, 1, 14), 12),
    ],
)
def test_time_slot_creation_count(location_count, start, end, expected_count, location_no_db):
    time_slots = m.TimeSlot.objects._make_time_slots(
        [location_no_db] * location_count, start, end, dt.timedelta(minutes=30), True, 100
    )
    assert len(time_slots) == expected_count


@pytest.mark.django_db
def test_time_slot_api_filtering(api_client, location, location2, monkeypatch):
    monkeypatch.setattr(timezone, "now", lambda: maw(dt.datetime(2020, 1, 1, 12)))
    day1 = timezone.now()
    day2 = day1 + dt.timedelta(days=1)
    m.TimeSlot.objects.create(location=location, start=day1, end=day1, is_active=True)
    m.TimeSlot.objects.create(location=location, start=day2, end=day2, is_active=True)
    m.TimeSlot.objects.create(location=location2, start=day1, end=day1, is_active=True)
    m.TimeSlot.objects.create(location=location2, start=day1, end=day1, is_active=False)

    rv = api_client.get(reverse("timeslot-list"))
    assert rv.status_code == status.HTTP_200_OK
    assert len(rv.data) == 3
    assert all([slot["is_active"] for slot in rv.data])

    rv = api_client.get(reverse("timeslot-list") + "?location=" + str(location.pk))
    assert rv.status_code == status.HTTP_200_OK, rv.data
    assert len(rv.data) == 2

    rv = api_client.get(reverse("timeslot-list") + "?location=" + str(location2.pk))
    assert rv.status_code == status.HTTP_200_OK, rv.data
    assert len(rv.data) == 1

    rv = api_client.get(reverse("timeslot-list") + "?start_date=" + day1.isoformat())
    assert rv.status_code == status.HTTP_200_OK, rv.data
    assert len(rv.data) == 2

    rv = api_client.get(reverse("timeslot-list") + "?start_date=" + day2.isoformat())
    assert rv.status_code == status.HTTP_200_OK, rv.data
    assert len(rv.data) == 1

    rv = api_client.get(
        reverse("timeslot-list") + "?start_date=" + day2.isoformat() + "&location=" + str(location2.pk)
    )
    assert rv.status_code == status.HTTP_200_OK, rv.data
    assert len(rv.data) == 0


@pytest.mark.django_db
def test_patch_appointment_with_time_slot(api_client, appointment, location, seat):
    start = timezone.now() + dt.timedelta(days=1)
    time_slot = m.TimeSlot.objects.create(start=start, end=start, location=location, is_active=True, capacity=10)
    rv = api_client.patch(
        reverse("appointment-detail", kwargs={"pk": appointment.pk}),
        {"time_slot": reverse("timeslot-detail", kwargs={"pk": time_slot.pk})},
    )
    assert rv.status_code == status.HTTP_200_OK, rv.data
    appointment.refresh_from_db()
    time_slot.refresh_from_db()
    assert appointment.time_slot == time_slot
    assert time_slot.usage == 1
    assert appointment.start == time_slot.start
    assert appointment.end == time_slot.end


@pytest.mark.django_db
@pytest.mark.parametrize(
    "slot_start, start_date, expected",
    [
        (dt.datetime(2020, 1, 1, 23, 1, tzinfo=pytz.UTC), "2020-01-02T00:15:00+01:00", 1),
        (dt.datetime(2020, 1, 1, 23, 1, tzinfo=pytz.UTC), "2020-01-02T00:15:00+00:00", 0),
        (dt.datetime(2020, 1, 1, 12, tzinfo=pytz.UTC), "2020-01-02T00:15:00+01:00", 0),
        (dt.datetime(2020, 1, 1, 12, tzinfo=pytz.UTC), "2020-01-02T00:15:00+00:00", 0),
        (dt.datetime(2020, 1, 1, 12, tzinfo=pytz.UTC), "2020-01-01T00:15:00+01:00", 1),
        (dt.datetime(2020, 1, 1, 12, tzinfo=pytz.UTC), "2020-01-01T00:15:00+00:00", 1),
    ],
)
def test_time_slot_filter_for_date(slot_start, start_date, expected, api_client, location, monkeypatch):
    time_slot = m.TimeSlot.objects.create(
        start=slot_start, end=slot_start + dt.timedelta(minutes=15), location=location
    )

    date_filter = f"?start_date={start_date}"
    rv = api_client.get((reverse("timeslot-list") + date_filter))
    assert rv.status_code == status.HTTP_200_OK, rv.data
    assert len(rv.data) == expected


@pytest.mark.django_db
def test_exclude_appointments_with_no_enough_capacity(api_client, location):
    m.TimeSlot.objects.create(start=timezone.now(), end=timezone.now(), capacity=10, usage=8, location=location)

    rv = api_client.get(reverse("timeslot-list"))
    assert rv.status_code == status.HTTP_200_OK
    assert len(rv.data) == 1

    rv = api_client.get(reverse("timeslot-list") + "?min_availability=3")
    assert rv.status_code == status.HTTP_200_OK
    assert len(rv.data) == 0

    rv = api_client.get(reverse("timeslot-list") + "?min_availability=2")
    assert rv.status_code == status.HTTP_200_OK
    assert len(rv.data) == 1


@pytest.mark.django_db
def test_forbid_taken_timeslot(api_client, location, appointment, seat):
    start = timezone.now() + dt.timedelta(days=1)
    slot = m.TimeSlot.objects.create(start=start, end=start, capacity=10, usage=10, location=location)
    rv = api_client.patch(
        reverse("appointment-detail", kwargs={"pk": appointment.pk}),
        {"time_slot": reverse("timeslot-detail", kwargs={"pk": slot.pk})},
    )
    assert rv.status_code == status.HTTP_400_BAD_REQUEST
    assert "time_slot" in rv.data


@pytest.mark.django_db
def test_forbid_timeslot_in_the_past(api_client, location, appointment):
    start = timezone.now()
    slot = m.TimeSlot.objects.create(start=start, end=start, capacity=10, usage=10, location=location)
    rv = api_client.patch(
        reverse("appointment-detail", kwargs={"pk": appointment.pk}),
        {"time_slot": reverse("timeslot-detail", kwargs={"pk": slot.pk})},
    )
    assert rv.status_code == status.HTTP_400_BAD_REQUEST
    assert rv.data["time_slot"] == "You can not choose time slots started in the past"

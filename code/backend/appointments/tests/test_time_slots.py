import datetime as dt

import pytest
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
def test_time_slot_api_filtering(api_client, location, location2):
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

    rv = api_client.get(reverse("timeslot-list") + "?start_date=" + day1.strftime("%Y-%m-%d"))
    assert rv.status_code == status.HTTP_200_OK, rv.data
    assert len(rv.data) == 2

    rv = api_client.get(reverse("timeslot-list") + "?start_date=" + day2.strftime("%Y-%m-%d"))
    assert rv.status_code == status.HTTP_200_OK, rv.data
    assert len(rv.data) == 1

    rv = api_client.get(
        reverse("timeslot-list") + "?start_date=" + day2.strftime("%Y-%m-%d") + "&location=" + str(location2.pk)
    )
    assert rv.status_code == status.HTTP_200_OK, rv.data
    assert len(rv.data) == 0

import datetime as dt

import pytest
from django.utils import timezone

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

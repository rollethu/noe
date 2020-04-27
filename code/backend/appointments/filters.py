import datetime as dt
import pytz
from django.db.models import F
from django.utils import timezone
from django_filters import fields
from django_filters import rest_framework as filters

from . import models as m


class SpaceTolerantIsoDateTimeField(fields.IsoDateTimeField):
    """
    Browsers by default replace `space` to `+` or `%20` in URIs.
    UTC offset `+01:00` comes in as ` 01:00` which is invalid.
    """

    def strptime(self, value, format):
        value = value.replace(" ", "+")
        return super().strptime(value, format)


class SpaceTolerantIsoDateTimeFilter(filters.IsoDateTimeFilter):
    field_class = SpaceTolerantIsoDateTimeField


class TimeSlotFilter(filters.FilterSet):
    start_date = SpaceTolerantIsoDateTimeFilter(method="filter_start_date")
    min_availability = filters.NumberFilter(method="filter_min_availability")

    class Meta:
        model = m.TimeSlot
        fields = ["location"]

    def filter_start_date(self, queryset, name, value):
        current_timezone = value.tzinfo

        day_start_in_timezone = value.replace(hour=0, minute=0, second=0, microsecond=0)

        day_start_in_utc = day_start_in_timezone.astimezone(pytz.UTC)
        day_end_in_utc = day_start_in_utc + dt.timedelta(days=1)

        return queryset.filter(start__range=[day_start_in_utc, day_end_in_utc])

    def filter_min_availability(self, queryset, name, value):
        return queryset.filter(capacity__gte=F("usage") + value)

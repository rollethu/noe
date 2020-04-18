from django_filters import rest_framework as filters

from . import models as m


class TimeSlotFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="start", lookup_expr="date")

    class Meta:
        model = m.TimeSlot
        fields = ["location"]

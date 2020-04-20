from django_filters import rest_framework as filters
from appointments.models import Appointment


class AppointmentFilter(filters.FilterSet):
    start_date = filters.DateFilter(field_name="start", lookup_expr="date")
    end_date = filters.DateFilter(field_name="end", lookup_expr="date")
    normalized_licence_plate = filters.CharFilter()

    class Meta:
        model = Appointment
        fields = ["start_date", "end_date", "normalized_licence_plate"]

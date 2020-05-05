from rest_framework import permissions
from . import models as m


class AppointmentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth is not None and isinstance(request.auth, m.Appointment)

    def has_object_permission(self, request, view, obj):
        get_appointment = getattr(view, "get_appointment", lambda obj: obj)
        appointment = get_appointment(obj)
        assert isinstance(appointment, m.Appointment)
        return request.auth == appointment

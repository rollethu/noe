from rest_framework import permissions


class AppointmentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return bool(getattr(request, "appointment", None))
        return True

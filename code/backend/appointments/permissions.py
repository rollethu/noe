from rest_framework import permissions


class AppointmentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth is not None

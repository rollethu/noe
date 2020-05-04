from rest_framework import permissions


class AppointmentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth is not None

    def has_object_permission(self, request, view, obj):
        return view.check_same_appointment(request, view, obj)

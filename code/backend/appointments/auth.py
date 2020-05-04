from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed
from . import models as m


class AppointmentAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Authorization: Apptoken <hashed value of Appointment UUID>
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        if auth_header is None:
            return None

        scheme, token = auth_header.split(" ")

        if scheme != "Apptoken":
            raise AuthenticationFailed()

        try:
            ev, signed_uuid = m.EmailVerification.objects.get_by_token(token)
        except m.EmailVerification.DoesNotExist:
            raise AuthenticationFailed()

        if ev.verified_at is None:
            raise AuthenticationFailed()

        # returns as (request.user, request.auth)
        return (None, ev.appointment)

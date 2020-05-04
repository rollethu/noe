from rest_framework import authentication


class AppointmentAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Authorization: Apptoken <hashed value of Appointment UUID>
        auth_header = request.META.get("HTTP_AUTHORIZATION")

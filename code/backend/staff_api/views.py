from django.urls import reverse as django_reverse
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework import routers, viewsets, mixins
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.reverse import reverse
from appointments.models import Appointment, Seat
from payments.models import Payment
from . import serializers as s
from . import filters as f
from .permissions import StaffApiPermissions


class StaffAPIRoot(routers.APIRootView):
    """
    REST API endpoints for staff members.
    """

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied()
        return super().get(request, *args, **kwargs)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        location_url = reverse("location-detail", kwargs={"pk": user.location.pk}, request=request)
        group = self._get_group_or_fail(user)
        return Response({"token": token.key, "location": location_url, "group": group.name})

    def _get_group_or_fail(self, user):
        try:
            return user.groups.get()
        except ObjectDoesNotExist:
            raise AuthenticationFailed("User has no groups")
        except MultipleObjectsReturned:
            raise AuthenticationFailed("User has multiple groups")


class AppointmentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [StaffApiPermissions]
    queryset = Appointment.objects.all()
    serializer_class = s.AppointmentSerializer
    filterset_class = f.AppointmentFilter


class SeatViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [StaffApiPermissions]
    queryset = Seat.objects.all()
    serializer_class = s.SeatSerializer

    def retrieve(self, request, *args, **kwargs):
        # request.auth is set only on Token authentication
        # When logged in through the api browser, only request.user will be set
        token_authenticated = request.auth is not None

        # the ?format=api or ?format=json URL query parameter will be set
        # when using the top right dropdown button next "GET"
        api_browser_format_param = "format" in request.GET

        if token_authenticated or api_browser_format_param:
            # business as usual, return the resource with the appropriate renderer
            return super().retrieve(request)

        # Redirect the logged-in user to the Seat admin page
        return redirect(django_reverse("admin:appointments_seat_change", kwargs={"object_id": kwargs["pk"]}))


class PaymentViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = [StaffApiPermissions]
    queryset = Payment.objects.all()
    serializer_class = s.PaymentSerializer

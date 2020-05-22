from urllib.parse import urlparse
from django.urls import resolve
from django.db import transaction
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework import mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from online_payments.payments.simple_v2 import SimplePay
from online_payments.payments.simple_v2.exceptions import IPNError
from online_payments.payments.exceptions import InvalidSignature

from appointments.models import Appointment, QRCode
from appointments.auth import AppointmentAuthentication
from appointments.permissions import AppointmentPermission
from appointments import email
from billing import serializers as bs
from feature_flags import use_feature_simplepay
from .prices import calc_payments, PRODUCTS, PaymentMethodType
from . import models as m
from . import serializers as s
from . import services


simplepay = SimplePay(settings.SIMPLEPAY_SECRET_KEY, settings.SIMPLEPAY_MERCHANT, settings.SIMPLEPAY_CALLBACK_URL)


class GetPriceView(generics.GenericAPIView):
    """Query the price of the Appointment.
    Get the Appointment ID in POST request body, so we don't leak it accidentally.
    """

    serializer_class = s.GetPriceSerializer
    authentication_classes = [AppointmentAuthentication]
    permission_classes = [AppointmentPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment, product = serializer.save()
        self.check_object_permissions(self.request, appointment)

        _, summary = calc_payments(appointment.seats.all(), product)
        return Response(summary)


class _BasePayView:
    def _complete_registration(self, appointment, payments):
        self._make_qrs(appointment.seats.all())
        # we need to refresh seats, because QR codes has been attached
        self._send_summaries(appointment.seats.all())

        # Appointment is done, when the payments are set.
        # This logic is moved from the frontend to here.
        # We consider appointments to be done even without
        # completed payments, including online incomplete payments.
        appointment.is_registration_completed = True
        appointment.save(update_fields=["is_registration_completed"])

    def _make_qrs(self, seats):
        for seat in seats:
            QRCode.objects.create(seat=seat)

    def _send_summaries(self, seats):
        for seat in seats:
            if not seat.email:
                raise ValidationError({"email": "Email field is required"})
            email.send_qrcode(seat)


class PayAppointmentView(_BasePayView, generics.GenericAPIView):
    """Called at the end of registration when user presses the Pay button."""

    serializer_class = s.PaySerializer
    authentication_classes = [AppointmentAuthentication]
    permission_classes = [AppointmentPermission]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        appointment, product = serializer.save()

        self.check_object_permissions(self.request, appointment)

        seats = appointment.seats.all()
        if len(seats) == 0:
            raise ValidationError({"appointment": "This appointment has no persons yet!"})

        existing_payments = []
        for seat in seats:
            payment = getattr(seat, "payment", None)
            if payment:
                existing_payments.append(payment)

        # In the current flow the user can not update their billing details.
        # When a payment fails, the user is redirected to the payment methods
        # screen, where they can change billing details.
        # This is not the dedicated place for billing detail update, therefore
        # changes are ignored.
        if not hasattr(appointment, "billing_detail"):
            self._add_billing_details_to_appointment(appointment, request)

        payments, summary = calc_payments(seats, product)

        if len(existing_payments) == len(seats):
            payments = existing_payments
        else:
            m.Payment.objects.bulk_create(payments)

        # This is just a sanity check, so we don't calculate a wrong amount.
        # What we show on the frontend, should always match on the backend.
        if summary["total_price"] != serializer.validated_data["total_price"]:
            raise ValidationError({"total_price": "Invalid amount!"})

        if use_feature_simplepay and serializer.validated_data["payment_method"] == PaymentMethodType.SIMPLEPAY:
            transaction = self._create_transaction(summary["total_price"], summary["currency"])
            res = simplepay.start(
                customer_email=appointment.email, order_ref=str(appointment.pk), total=summary["total_price"]
            )

            transaction.status = transaction.STATUS_WAITING_FOR_AUTHORIZATION
            transaction.external_reference_id = res.transaction_id
            transaction.save()

            for payment in payments:
                payment.simplepay_transactions.add(transaction)

            return Response({"simplepay_form_url": res.payment_url})

        else:
            self._complete_registration(appointment, payments)
            return Response(summary)

    def _add_billing_details_to_appointment(self, appointment, request):
        serializer = bs.BillingDetailSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

    def _create_transaction(self, amount, currency):
        transaction = m.SimplePayTransaction.objects.create(amount=amount, currency=currency)
        return transaction


class PaymentStatusView(generics.GenericAPIView):
    authentication_classes = [AppointmentAuthentication]
    permission_classes = [AppointmentPermission]

    def get(self, request, *args, **kwargs):
        appointment = request.auth

        try:
            first_seat = appointment.seats.first()
            first_payment = first_seat.payment
            last_transaction = first_payment.simplepay_transactions.order_by("-created_at").first()
            if last_transaction is None:
                raise AttributeError
        except AttributeError:
            return Response({"error": True}, status=status.HTTP_400_BAD_REQUEST)

        payment_status = "ERROR"
        if last_transaction.status == last_transaction.STATUS_COMPLETED:
            payment_status = "SUCCESS"
        elif last_transaction.status == last_transaction.STATUS_WAITING_FOR_AUTHORIZATION:
            payment_status = "PENDING"
        return Response({"payment_status": payment_status})


@api_view(["POST"])
def simplepay_v2_callback_view(request):
    try:
        ipn, response = simplepay.process_ipn_request(request)
    except (InvalidSignature, IPNError):
        raise ValidationError({"error": _("SimplePay error")})

    transaction = m.SimplePayTransaction.objects.get(external_reference_id=ipn.transaction_id)
    if ipn.status == "FINISHED":
        services.complete_transaction(transaction, ipn.finish_date)
    return Response(response["body"], headers=response["headers"])

import os
import base64
import json
from urllib.parse import urljoin, urlencode
from django.db import transaction
from django.urls import reverse
from django.conf import settings
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from appointments.auth import AppointmentAuthentication
from appointments.permissions import AppointmentPermission
from payments import serializers as payments_serializers
from payments.views import _BasePayView
from online_payments.payments.simple_v2 import SimplePay, SimplePayEvent
from online_payments.payments.simple_v2.exceptions import IPNError, SimplePayException
from online_payments.payments.exceptions import InvalidSignature
from online_payments.billing.szamlazzhu.exceptions import SzamlazzhuError
from . import models as m
from .config import simplepay_config


ROUTE_PAYMENT_STATUS = "/fizetes-status"
ROUTE_PAYMENT_FAILED = "/sikertelen-fizetes"


simplepay = SimplePay(simplepay_config.secret_key, simplepay_config.merchant, simplepay_config.use_live)


class PayAppointmentSimplePayView(_BasePayView):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        appointment, payments, summary = self._handle_payment(request)
        transaction = m.SimplePayTransaction.objects.create(
            amount=summary["total_price"], currency=summary["currency"]
        )

        # Order ref must be unique at a transaction level, appointment level is not enough.
        # When multiple transactions with the same order refs are sent to Simple,
        # Simple will find the same transaction.
        # It is even possible to put a transaction from Cancelled to Created state
        # in Simple's system, by creating and sending a start request with the same order_ref.
        order_ref = str(transaction.pk)
        try:
            res = simplepay.start(
                customer_email=appointment.email,
                order_ref=order_ref,
                total=summary["total_price"],
                callback_url=request.build_absolute_uri(reverse("simplepay-back")),
            )
        except SimplePayException as error:
            raise ValidationError({"error": str(error)})

        transaction.status = transaction.STATUS_WAITING_FOR_AUTHORIZATION
        transaction.external_reference_id = res.transaction_id
        transaction.save()

        for payment in payments:
            payment.simplepay_transactions.add(transaction)

        return Response({"simplepay_form_url": res.payment_url})


@api_view(["POST"])
def simplepay_ipn_view(request):
    try:
        ipn, response = simplepay.process_ipn_request(request)
    except (InvalidSignature, IPNError):
        raise ValidationError({"error": _("SimplePay error")})

    transaction = m.SimplePayTransaction.objects.get(external_reference_id=ipn.transaction_id)
    if ipn.status == "FINISHED":
        try:
            transaction.complete(ipn.finish_date)
        except SzamlazzhuError as e:
            raise ValidationError({"error": str(e)})

    return Response(response["body"], headers=response["headers"])


@api_view(["GET"])
def simplepay_back_view(request):
    """docs: PaymentService v2 - 3.11 back url"""

    expected_signature = request.GET["s"]
    r_params_json = base64.b64decode(request.GET["r"].encode())
    simplepay.validate_signature(expected_signature, r_params_json.decode())

    r_params = json.loads(r_params_json)
    event = SimplePayEvent(r_params["e"])
    if event is SimplePayEvent.SUCCESS:
        frontend_path = ROUTE_PAYMENT_STATUS
    else:
        frontend_path = ROUTE_PAYMENT_FAILED

    frontend_full_url = urljoin(settings.FRONTEND_URL, frontend_path)

    transaction_params = {
        "simplepay_transaction_id": r_params["t"],
        "simplepay_transaction_event": event.value,
    }
    return redirect(f"{frontend_full_url}?{urlencode(transaction_params)}")

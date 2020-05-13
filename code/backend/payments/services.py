import datetime as dt
from django.utils.translation import gettext as _

from billing import services as billing_services


MISSING = object()


def validate_paid_at(payment, all_data: dict):
    new_paid_at = all_data.get("paid_at", MISSING)
    if new_paid_at is MISSING:
        return

    original_paid_at = payment.paid_at
    if original_paid_at and new_paid_at != original_paid_at:
        raise ValueError(_("Paid at can not be changed"))


def handle_paid_at(payment, all_data: dict):
    try:
        validate_paid_at(payment, all_data)
    except ValueError:
        return

    if payment.paid_at is None and all_data.get("paid_at"):
        billing_services.send_invoice(payment.seat)

import datetime as dt
from django.utils.translation import gettext as _

from billing import services as billing_services


MISSING = object()


def validate_paid_at(original_paid_at, all_data: dict):
    new_paid_at = all_data.get("paid_at", MISSING)
    if new_paid_at is MISSING:
        return

    if original_paid_at and new_paid_at != original_paid_at:
        raise ValueError(_("Paid at can not be changed"))


def handle_paid_at(original_paid_at, seat, all_data: dict):
    try:
        validate_paid_at(original_paid_at, all_data)
    except ValueError:
        return

    if original_paid_at is None and all_data.get("paid_at"):
        billing_services.send_invoice(seat)

import datetime as dt
from django.utils.translation import gettext as _
from django.apps import apps as django_apps


MISSING = object()

# submitted_data can be one of:
# - serializer.validated_data (staff_api)
# - form.cleaned_data (PaymentInline admin)
def validate_paid_at(original_paid_at, submitted_data: dict):
    new_paid_at = submitted_data.get("paid_at", MISSING)
    if new_paid_at is MISSING:
        return

    if original_paid_at and new_paid_at != original_paid_at:
        raise ValueError(_("Paid at can not be changed"))


def handle_paid_at(original_paid_at, seat, submitted_data: dict):
    try:
        validate_paid_at(original_paid_at, submitted_data)
    except ValueError:
        return

    if original_paid_at is None and submitted_data.get("paid_at"):
        billing = django_apps.get_app_config("billing")
        billing.service.send_seat_invoice(seat)

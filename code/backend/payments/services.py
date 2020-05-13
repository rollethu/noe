from django.utils.translation import gettext as _

from billing import services as billing_services


def validate_paid_at(payment, all_data: dict):
    """
    `all_data` can be on of:
    - serializer.validated_data (staff_api)
    - form.cleaned_data (PaymentInline admin)
    """

    new_paid_at = all_data.get("paid_at", False)  # False to tell apart from explicit None
    if new_paid_at is False:
        return False

    if payment.paid_at and new_paid_at is not False and new_paid_at != payment.paid_at:
        raise ValueError(_("Paid at can not be changed"))

    if new_paid_at is None:
        return False

    return True


def handle_paid_at(payment, all_data: dict):
    can_send = validate_paid_at(payment, all_data)
    if can_send:
        billing_services.send_invoice(payment.seat)

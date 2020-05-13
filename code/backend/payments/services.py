from django.utils.translation import gettext as _

from billing import services as billing_services


def _handle_paid_at(payment, all_data):
    new_paid_at = all_data.get("paid_at", False)  # False to tell apart from explicit None
    if new_paid_at is False:
        return

    if payment.paid_at and new_paid_at is not False:
        raise ValueError({"paid_at": _("Paid at can not be changed")})

    if new_paid_at is None:
        return

    billing_services.send_invoice(payment.seat)

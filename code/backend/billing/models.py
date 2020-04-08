import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Bill(models.Model):
    BILL_TYPE_RECEIPT = "RECEIPT"
    BILL_TYPE_VAT_INVOICE = "VAT_INVOICE"
    BILL_TYPE_CHOICES = (
        (BILL_TYPE_RECEIPT, _("receipt")),
        (BILL_TYPE_VAT_INVOICE, _("VAT invoice")),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment = models.ForeignKey(
        "appointments.Appointment", on_delete=models.SET_NULL, null=True
    )
    payment = models.ForeignKey(
        "payments.Payment", on_delete=models.SET_NULL, null=True
    )

    bill_id = models.CharField(max_length=255, default="")
    bill_type = models.CharField(max_length=255, choices=BILL_TYPE_CHOICES)

    class Meta:
        ordering = ("created_at",)


class BillingDetail(models.Model):
    """Only saved when a VAT invoice is requested during online payment."""

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment = models.OneToOneField(
        "appointments.Appointment", on_delete=models.CASCADE
    )

    company_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    post_code = models.CharField(max_length=255)
    state = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    tax_number = models.CharField(max_length=255)

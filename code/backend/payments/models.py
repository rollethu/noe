import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from .prices import PaymentMethodType


class Payment(models.Model):
    PAYMENT_METHOD_TYPE_CHOICES = (
        (PaymentMethodType.SIMPLEPAY, _("SimplePay")),
        (PaymentMethodType.ON_SITE, _("On-site")),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seat = models.ForeignKey("appointments.Seat", on_delete=models.SET_NULL, null=True)
    simplepay_transaction = models.ForeignKey(
        "SimplePayTransaction", on_delete=models.SET_NULL, blank=True, null=True, related_name="payments"
    )
    payment_method_type = models.CharField(max_length=255, choices=PAYMENT_METHOD_TYPE_CHOICES)
    amount = models.FloatField()
    currency = models.CharField(max_length=3, default="HUF")
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(
        blank=True, null=True, help_text=_("When this field is empty, no payment for the person has been made (yet)."),
    )
    proof_number = models.CharField(
        blank=True,
        max_length=255,
        help_text=_(
            "Printed receipt/bill number, healthcare number (TAJ kártya szám) "
            "or anything which proves this payment has been made."
        ),
    )
    note = models.TextField(blank=True, help_text=_("Anything important to note about this payment."))

    class Meta:
        ordering = ("created_at",)


class SimplePayTransaction(models.Model):
    STATUS_CREATED = "CREATED"
    STATUS_WAITING_FOR_AUTHORIZATION = "WAITING_FOR_AUTHORIZATION"
    STATUS_AUTHORIZED = "AUTHORIZED"
    STATUS_WAITING_FOR_COMPLETION = "WAITING_FOR_COMPLETION"
    STATUS_COMPLETED = "COMPLETED"
    STATUS_WAITING_FOR_REFUND = "WAITING_FOR_REFUND"
    STATUS_REFUNDED = "REFUNDED"
    STATUS_REJECTED = "REJECTED"
    STATUS_CANCELLED = "CANCELLED"
    STATUS_CHOICES = [
        (STATUS_CREATED, _("created")),
        (STATUS_WAITING_FOR_AUTHORIZATION, _("waiting for authorization")),
        (STATUS_AUTHORIZED, _("authorized")),
        (STATUS_WAITING_FOR_COMPLETION, _("waiting for completion")),
        (STATUS_COMPLETED, _("completed")),
        (STATUS_WAITING_FOR_REFUND, _("waiting for refund")),
        (STATUS_REFUNDED, _("refunded")),
        (STATUS_REJECTED, _("rejected")),
        (STATUS_CANCELLED, _("cancelled")),
    ]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.FloatField()
    currency = models.CharField(max_length=3, default="HUF")
    external_reference_id = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_CREATED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "SimplePay transaction"
        verbose_name_plural = "SimplePay transactions"

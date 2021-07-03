import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from .prices import PaymentMethodType, PAYMENT_METHOD_TYPE_CHOICES, PRODUCTS, PRODUCT_CHOICES


class Payment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seat = models.OneToOneField("appointments.Seat", on_delete=models.SET_NULL, null=True)
    simplepay_transactions = models.ManyToManyField(
        "simplepay.SimplePayTransaction", blank=True, null=True, related_name="payments"
    )
    payment_method_type = models.CharField(max_length=255, choices=PAYMENT_METHOD_TYPE_CHOICES)
    product_type = models.CharField(max_length=50, choices=PRODUCT_CHOICES)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
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

    @property
    def is_paid(self):
        return self.paid_at is not None

    @property
    def product(self):
        return PRODUCTS[self.product_type]

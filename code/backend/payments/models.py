import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Payment(models.Model):
    PAYMENT_METHOD_TYPE_SIMPLEPAY = "SIMPLEPAY"
    PAYMENT_METHOD_TYPE_ON_SITE = "ON_SITE"
    PAYMENT_METHOD_TYPE_CHOICES = (
        (PAYMENT_METHOD_TYPE_SIMPLEPAY, _("SimplePay")),
        (PAYMENT_METHOD_TYPE_ON_SITE, _("On-site")),
    )
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seat = models.ForeignKey("appointments.Seat", on_delete=models.SET_NULL, null=True)
    payment_method_type = models.CharField(
        max_length=255, choices=PAYMENT_METHOD_TYPE_CHOICES
    )
    amount = models.FloatField()
    currency = models.CharField(max_length=3, default="HUF")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)


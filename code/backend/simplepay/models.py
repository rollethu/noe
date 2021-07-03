import uuid
from django.apps import apps as django_apps
from django.db import models, transaction
from django.utils.translation import gettext_lazy as _
from appointments.models import QRCode
from appointments import email
from rest_framework.exceptions import ValidationError


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
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.CharField(max_length=3, default="HUF")
    external_reference_id = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_CREATED)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "SimplePay transaction"
        verbose_name_plural = "SimplePay transactions"

    @transaction.atomic
    def complete(self, finish_date):
        # This happens in the context of SimplePay payment for the entire appointment.
        self.status = self.STATUS_COMPLETED
        self.save()

        # any payment and seat are ok to find the right appointment
        appointment = self.payments.first().seat.appointment
        appointment.is_registration_completed = True
        appointment.save()

        self.payments.all().update(paid_at=finish_date)

        for seat in appointment.seats.all():
            QRCode.objects.create(seat=seat)

        # Need to query seats again
        for seat in appointment.seats.all():
            if not seat.email:
                raise ValidationError({"email": "Email field is required"})
            email.send_qrcode(seat)

        billing = django_apps.get_app_config("billing")
        billing.service.send_appointment_invoice(appointment)

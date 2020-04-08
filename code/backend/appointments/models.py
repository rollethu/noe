import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ("created_at",)


class Appointment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(Location, on_delete=models.PROTECT)

    phone_number = models.CharField(
        max_length=30, help_text=_("Primary communication channel with the patient.")
    )
    email = models.EmailField(
        blank=True,
        help_text=_(
            "Only used for online payments with Simple, invoice and billing for now."
        ),
    )
    gtc = models.CharField(
        max_length=10,
        help_text=_(
            "Accepted version of General Terms and Conditions. "
            "Applied to everyone whose Seat belong to this Appointment."
        ),
    )
    privacy_policy = models.CharField(
        max_length=10,
        help_text=_(
            "Accepted version of privacy policy. "
            "Applied to everyone whose Seat belong to this Appointment."
        ),
    )
    start = models.DateTimeField(
        help_text=_("The appointment is valid from this time.")
    )
    end = models.DateTimeField(
        help_text=_(
            "The appointment is valid until this time. "
            "This probably should be handled more lightly than the start time."
        )
    )

    class Meta:
        ordering = ("created_at",)


class PhoneVerification(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    verified_at = models.DateTimeField()
    code = models.CharField(max_length=255)

    @property
    def is_verified(self):
        return self.verified_at is not None

    class Meta:
        ordering = ("created_at",)


class Seat(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    healthcare_number = models.CharField(max_length=30)
    identity_card_number = models.CharField(max_length=30)
    post_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=200, help_text="Street address")
    address_line2 = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("Apartment, building, floor, suite, door, etc..."),
    )
    has_doctor_referral = models.BooleanField(default=False)
    paid_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "When this field is empty, no payment for the person has been made (yet)."
        ),
    )

    class Meta:
        ordering = ("created_at",)

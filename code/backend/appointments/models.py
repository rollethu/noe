import uuid
import string
import secrets
import datetime as dt
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.utils.translation import gettext_lazy as _
from django.core.signing import Signer
from django.utils import timezone
from cryptography.fernet import Fernet


encrypter = Fernet(settings.EMAIL_VERIFICATION_KEY)


class Location(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=100)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("created_at",)


class AppointmentManager(models.Manager):
    def create(self, *args, **kwargs):
        appointment = super().create(*args, **kwargs)
        ev = EmailVerification(appointment=appointment)
        ev.save()
        return appointment


class Appointment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name="appointments", blank=True, null=True,
    )

    phone_number = models.CharField(max_length=30, blank=True)
    licence_plate = models.CharField(max_length=30, blank=True)
    normalized_licence_plate = models.CharField(max_length=30, blank=True)
    email = models.EmailField(help_text=_("Primary communication channel with the patient."))
    gtc = models.CharField(
        max_length=10,
        help_text=_(
            "Accepted version of General Terms and Conditions. "
            "Applied to everyone whose Seat belong to this Appointment."
        ),
    )
    privacy_policy = models.CharField(
        max_length=10,
        help_text=_("Accepted version of privacy policy. Applied to everyone whose Seat belong to this Appointment."),
    )
    start = models.DateTimeField(blank=True, null=True, help_text=_("The appointment is valid from this time."))
    end = models.DateTimeField(
        blank=True,
        null=True,
        help_text=_(
            "The appointment is valid until this time. "
            "This probably should be handled more lightly than the start time."
        ),
    )
    is_registration_completed = models.BooleanField(
        default=False, help_text='Set before the user is redirected to the "Successful registration" page'
    )
    time_slot = models.ForeignKey("TimeSlot", blank=True, null=True, on_delete=models.SET_NULL)

    objects = AppointmentManager()

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        if self.start:
            return f"{self.location} - {self.start:%Y-%m-%d %H:%M}"
        else:
            return f"{self.location} - in progress"


class PhoneVerification(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="phone_verifications")

    verified_at = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.appointment.phone_number}: {self.code}"

    class Meta:
        ordering = ("created_at",)

    @property
    def is_verified(self):
        return self.verified_at is not None


def _generate_email_code():
    # https://docs.python.org/3/library/secrets.html#recipes-and-best-practices
    # example asdf234
    alphanumeric = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphanumeric) for _ in range(20))


class EmailVerificationManager(models.Manager):
    def get_by_token(self, token: str):
        signed_uuid_bytes = encrypter.decrypt(token.encode())
        signed_uuid = signed_uuid_bytes.decode()
        uuid = signed_uuid.split(":", 1)[0]
        ev = self.model.objects.get(uuid=uuid)
        return ev, signed_uuid


class EmailVerification(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="email_verifications")
    verified_at = models.DateTimeField(blank=True, null=True)
    code = models.CharField(max_length=255, default=_generate_email_code)

    objects = EmailVerificationManager()

    class Meta:
        ordering = ("created_at",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # code and SECRET_KEY will be needed to validate
        self._signer = Signer(salt=self.code)

    def make_token(self) -> str:
        signed_uuid = self._signer.sign(self.uuid)
        return encrypter.encrypt(signed_uuid.encode()).decode()

    def verify(self, signed_uuid: str):
        if self.is_verified:
            raise ValueError("The email has been verified already.")
        valid_uuid = uuid.UUID(self._signer.unsign(signed_uuid))
        success = valid_uuid == self.uuid
        if success:
            self.verified_at = timezone.now()
            self.save()
        return success

    @property
    def is_verified(self):
        return self.verified_at is not None


class Seat(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="seats")

    full_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    healthcare_number = models.CharField(blank=True, max_length=30)
    identity_card_number = models.CharField(max_length=30)
    post_code = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    address_line1 = models.CharField(max_length=200, help_text="Street address")
    address_line2 = models.CharField(
        max_length=200, blank=True, help_text=_("Apartment, building, floor, suite, door, etc..."),
    )
    has_doctor_referral = models.BooleanField(default=False)
    email = models.EmailField(help_text=_("Notification email for the test results."))
    phone_number = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"{self.full_name} - {self.appointment}"

    @property
    def full_address(self):
        return f"{self.post_code} {self.city}, {self.address_line1} {self.address_line2}"


def generate_uuid():
    return uuid.uuid4().hex


class QRCode(models.Model):
    LOCATION_DIGITS = 4
    DAY_SERIAL_DIGITS = 4

    seat = models.OneToOneField(Seat, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    # We need the id to be set, which will only be available after save. In
    # order to allow the unique constraint, first we make a random string which
    # makes it possible to save, but keep the field unique. Otherwise, we would
    # need to save first with empty string default and calculate the real code
    # after that, which would make IntegrityErrors possible.
    code = models.CharField(max_length=40, unique=True, default=generate_uuid)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        new_object = self.pk is None
        # we need to save first to get the id
        super().save(*args, **kwargs)
        # We don't want this to change after it has been set
        if new_object:
            self.code = self._calc_code()
            super().save(update_fields=["code"])

    def _calc_code(self):
        # https://gitlab.com/rollet/project-noe/-/wikis/Seat-QR-codes
        try:
            location_pk_str = str(self.seat.appointment.location.pk)
        except AttributeError:
            # appointment has no Location
            location_pk_str = "0" * self.LOCATION_DIGITS
        location_id = location_pk_str.zfill(self.LOCATION_DIGITS)

        # This needs to be localtime, so can be verified by just looking at it
        localdt = timezone.localtime()
        local_date = localdt.strftime("%y%m%d")

        modulus = 10 ** (self.DAY_SERIAL_DIGITS + 1)
        day_serial = str(self.pk % modulus).zfill(self.DAY_SERIAL_DIGITS)

        return f"{location_id}-{local_date}-{day_serial}"

    def get_absolute_url(self):
        return reverse("qrcode", args=[str(self.code)])


class TimeSlotManager(models.Manager):
    def create_time_slots(
        self, locations, start, end, duration, is_active=True, capacity=settings.DEFAULT_TIME_SLOT_CAPACITY,
    ):
        time_slots = self._make_time_slots(locations, start, end, duration, is_active, capacity)
        TimeSlot.objects.bulk_create(time_slots)

    @staticmethod
    def _make_time_slots(locations, start, end, duration, is_active, capacity):
        """
        Creates multiple TimeSlots.

        A new TimeSlot still can be created if its end would go past the `end` parameter.
        """

        time_slots = []
        for location in locations:
            current_time = start
            while current_time < end:
                next_time = current_time + duration
                time_slot = TimeSlot(
                    location=location, start=current_time, end=next_time, is_active=is_active, capacity=capacity
                )
                time_slots.append(time_slot)
                current_time = next_time
        return time_slots


class TimeSlot(models.Model):
    """
    TimeSlots represent a Location specific time, that can be booked for
    Slots.

    The number of Seats can fit in a Slot is determined by the `capacity`
    attribute.
    Ideally, new Seats can only be added to a TimeSlot if its `usage` is less
    than its capacity.

    TimeSlots are created ahead of time by a member of staff of Project Noe.
    """

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.ForeignKey("Location", on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    capacity = models.IntegerField(default=0, help_text=_("Determines how many Seats can book for this period."))
    usage = models.IntegerField(
        default=0, help_text=_("Number of Seats who booked for this period. This should't be edited by humans :)"),
    )
    is_active = models.BooleanField(
        default=True, help_text=_("Time Slot is only availabe to be booked for if active."),
    )

    objects = TimeSlotManager()

    class Meta:
        ordering = ("created_at",)

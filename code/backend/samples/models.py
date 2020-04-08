import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Sample(models.Model):
    """
    Sample is what's extracted from a real person to be examined in the lab,
    to determine whether or not the persion is infected.
    """

    SAMPLE_STATUS_EMPTY = "EMPTY"
    SAMPLE_STATUS_SAMPLED = "SAMPLED"
    SAMPLE_STATUS_IN_TRANSPORT = "IN_TRANSPORT"
    SAMPLE_STATUS_WAITING_IN_LAB = "WAITING_IN_LAB"
    SAMPLE_STATUS_EXAMINED = "EXAMINED"
    SAMPLE_STATUS_CHOICES = (
        (SAMPLE_STATUS_EMPTY, _("empty")),
        (SAMPLE_STATUS_SAMPLED, _("sampled")),
        (SAMPLE_STATUS_IN_TRANSPORT, _("in transport")),
        (SAMPLE_STATUS_WAITING_IN_LAB, _("waiting in lab")),
        (SAMPLE_STATUS_EXAMINED, _("examined")),
    )

    RESULT_STATUS_POSITIVE = "POSITIVE"
    RESULT_STATUS_NEGATIVE = "NEGATIVE"
    RESULT_STATUS_NOT_TESTED_YET = "NOT_TESTED_YET"
    RESULT_STATUS_CHOICES = (
        (RESULT_STATUS_POSITIVE, _("positive")),
        (RESULT_STATUS_NEGATIVE, _("negative")),
        (RESULT_STATUS_NOT_TESTED_YET, _("not tested yet")),
    )

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    seat = models.ForeignKey(
        "appointments.Seat", on_delete=models.SET_NULL, null=True, blank=True
    )
    sampled_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The time when it is extraxted from a real person",
    )
    location = models.ForeignKey(
        "appointments.Location", on_delete=models.SET_NULL, null=True
    )
    status = models.CharField(
        max_length=255, choices=SAMPLE_STATUS_CHOICES, default=SAMPLE_STATUS_EMPTY
    )
    result = models.CharField(
        max_length=255,
        choices=RESULT_STATUS_CHOICES,
        default=RESULT_STATUS_NOT_TESTED_YET,
    )
    created_at = models.DateTimeField(auto_now_add=True)

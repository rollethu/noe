import uuid

from django.db import models


class SurveyQuestion(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_required = models.BooleanField(default=True)
    answer_datatype = models.CharField(max_length=255, default="string")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)


class SurveyAnswer(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey("SurveyQuestion", null=True, on_delete=models.SET_NULL)
    seat = models.ForeignKey("appointments.Seat", null=True, on_delete=models.SET_NULL)
    answer = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

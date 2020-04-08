import uuid

from django.db import models


class SurveyQuestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=False)
    is_required = models.BooleanField(default=True)
    answer_datatype = models.CharField(default='string')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at', )


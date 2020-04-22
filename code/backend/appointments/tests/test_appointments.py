import pytest
from rest_framework.reverse import reverse
from rest_framework import status

from appointments import models as m


@pytest.mark.django_db
def test_licence_plate_normalization(api_client, appointment):
    rv = api_client.patch(reverse("appointment-detail", kwargs={"pk": appointment.pk}), {"licence_plate": "abc-123"})
    assert rv.status_code == status.HTTP_200_OK
    assert rv.data["normalized_licence_plate"] == "ABC123"
    appointment.refresh_from_db()
    assert appointment.normalized_licence_plate == "ABC123"

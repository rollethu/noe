import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from appointments import models as m


@pytest.mark.django_db
def test_healthcare_number_is_required_if_has_referral(api_client, appointment):
    rv = api_client.post(
        reverse("seat-list"),
        {
            "appointment": reverse("appointment-detail", kwargs={"pk": appointment.pk}),
            "full_name": "Full Name",
            "birth_date": "1990-06-14",
            "post_code": "1234",
            "city": "Budapest",
            "address_line1": "Alpha street 8.",
            "identity_card_number": "123456AB",
            "email": "asd@asd.com",
            "has_doctor_referral": True,
        },
    )
    assert rv.status_code == status.HTTP_400_BAD_REQUEST
    assert "healthcare_number" in rv.data


@pytest.mark.django_db
def test_healthcare_number_is_not_required_without_has_referral(api_client, appointment):
    rv = api_client.post(
        reverse("seat-list"),
        {
            "appointment": reverse("appointment-detail", kwargs={"pk": appointment.pk}),
            "full_name": "Full Name",
            "birth_date": "1990-06-14",
            "post_code": "1234",
            "city": "Budapest",
            "address_line1": "Alpha street 8.",
            "identity_card_number": "123456AB",
            "email": "asd@asd.com",
        },
    )
    assert rv.status_code == status.HTTP_201_CREATED
    assert m.Seat.objects.count() == 1

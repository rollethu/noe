import pytest
from rest_framework import status
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_seat_detail_url_redirect_to_admin_without_header(staff_api_client, seat):
    rv = staff_api_client.get(reverse("staff-seat-detail", kwargs={"pk": seat.pk}))
    assert rv.status_code == status.HTTP_302_FOUND
    assert rv["location"] == reverse("admin:appointments_seat_change", kwargs={"object_id": seat.pk})


@pytest.mark.django_db
def test_seat_detail_returns_response_with_header(staff_api_client, seat):
    rv = staff_api_client.get(reverse("staff-seat-detail", kwargs={"pk": seat.pk}), HTTP_USE_STAFF_API="true")
    assert rv.status_code == status.HTTP_200_OK

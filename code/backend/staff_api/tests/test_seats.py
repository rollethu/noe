import pytest
from django.contrib.auth.models import Group, Permission
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APIClient
from users.models import User


@pytest.fixture
def api_user():
    group = Group.objects.create(name="seatgroup")
    p = Permission.objects.get(codename="view_seat")
    group.permissions.add(p)
    user = User.objects.create(username="testuser", password="testpassword", is_admin=True)
    user.groups.add(group)
    return user


@pytest.fixture
def staff_api_client(api_user, api_client):
    token = Token.objects.create(user=api_user)
    api_client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return api_client


@pytest.fixture
def staff_api_browser(api_user, api_client):
    # We simulate the user coming from the browser with Session authentication
    api_client.force_authenticate(user=api_user, token=None)
    return api_client


@pytest.mark.django_db
def test_seat_detail_url_redirect_to_admin(staff_api_browser, api_user, seat):
    seat_staff_api_url = reverse("staff-seat-detail", kwargs={"pk": seat.pk})
    rv = staff_api_browser.get(seat_staff_api_url)
    assert rv.status_code == status.HTTP_302_FOUND
    assert rv["location"] == reverse("admin:appointments_seat_change", kwargs={"object_id": seat.pk})


@pytest.mark.django_db
def test_seat_detail_returns_response_when_using_browsable_api(staff_api_browser, api_user, seat):
    seat_staff_api_url = reverse("staff-seat-detail", kwargs={"pk": seat.pk})
    http_get_params = {"format": "api"}
    rv = staff_api_browser.get(seat_staff_api_url, http_get_params)
    assert rv.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_seat_detail_returns_response_when_using_token_auth(staff_api_client, seat):
    seat_staff_api_url = reverse("staff-seat-detail", kwargs={"pk": seat.pk})
    rv = staff_api_client.get(seat_staff_api_url)
    assert rv.status_code == status.HTTP_200_OK

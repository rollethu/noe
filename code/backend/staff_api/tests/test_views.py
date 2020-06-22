import uuid
import pytest
from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse
from rest_framework import status
from ..views import LoginView


@pytest.mark.django_db
def test_succesful_login(factory, api_user):
    req = factory.post("/staff-api/login/", {"username": api_user.username, "password": api_user.PASSWORD})
    login_view = LoginView.as_view()
    res = login_view(req)
    assert len(res.data["token"]) == 40
    assert res.data["location"] == "http://testserver/api/locations/1/"
    assert res.data["group"] == "seatgroup"
    assert res.data["qrcode_location_prefix"] == "0001"


@pytest.mark.django_db
def test_traffic_control(api_user, staff_api_client):
    user_group = api_user.groups.get()
    p = Permission.objects.get(codename="view_appointment")
    user_group.permissions.add(p)

    res = staff_api_client.get("/staff-api/traffic-control/abc-123/")
    assert res.data["normalized_licence_plate"] == "ABC123"
    assert "is_paid" in res.data


@pytest.mark.django_db
def test_seat_doesnt_exist(staff_api_client):
    res = staff_api_client.get(reverse("staff-seat-detail", kwargs={"pk": uuid.uuid4()}))
    assert res.status_code == status.HTTP_404_NOT_FOUND

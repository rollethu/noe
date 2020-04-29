import datetime as dt
from pathlib import Path
from django.utils import timezone
import pytest
from .. import models as m

# QR code generation relies on primary_key being monotonic
pytestmark = pytest.mark.django_db


@pytest.fixture(autouse=True)
def mock_date(monkeypatch):
    monkeypatch.setattr(timezone, "localtime", lambda: dt.datetime(2020, 4, 22, 18, 42))


def test_qrcode_with_no_seat():
    qr = m.QRCode.objects.create()
    assert qr.code == "0000-200422-0001"

    qr2 = m.QRCode.objects.create()
    assert qr2.code == "0000-200422-0002"


def test_qrcode_appointment_with_no_location(seat):
    qr = m.QRCode.objects.create(seat=seat)
    assert qr.code == "0000-200422-0001"


def test_qrcode_appointment_with_location(location, appointment, seat):
    appointment.location = location
    qr = m.QRCode.objects.create(seat=seat)
    assert qr.code == "0001-200422-0001"

    seat2 = m.Seat.objects.create(birth_date=timezone.now(), appointment=appointment)
    qr2 = m.QRCode.objects.create(seat=seat2)
    assert qr2.code == "0001-200422-0002"


def test_qrcode_multiple_locations(location, appointment, seat):
    appointment.location = location
    qr = m.QRCode.objects.create(seat=seat)
    assert qr.code == "0001-200422-0001"

    location2 = m.Location.objects.create()
    appointment2 = m.Appointment.objects.create(location=location2)
    seat2 = m.Seat.objects.create(birth_date=timezone.now(), appointment=appointment2)
    qr2 = m.QRCode.objects.create(seat=seat2)
    assert qr2.code == "0002-200422-0002"


def test_absolute_url():
    qr = m.QRCode.objects.create()
    assert qr.get_absolute_url() == "/qrcode/0000-200422-0001/"

    qr2 = m.QRCode.objects.create()
    assert qr2.get_absolute_url() == "/qrcode/0000-200422-0002/"


class TestImageGeneration:
    def test_make_png(self, settings, datadir):
        settings.BACKEND_URL = "https://127.0.0.1:8000"
        qr = m.QRCode()
        qr.code = "0000-200423-0053"
        result = qr.make_png()
        assert type(result) is bytes
        expected = datadir.joinpath("qr-https-127.0.0.1-8000-code-0000-200423-0053.png").read_bytes()
        assert result == expected


def test_location_prefix():
    assert m.QRCode.get_location_prefix(None) == "0000"

    location = m.Location(pk=1)
    assert m.QRCode.get_location_prefix(location) == "0001"

    location = m.Location(pk=9999)
    assert m.QRCode.get_location_prefix(location) == "9999"

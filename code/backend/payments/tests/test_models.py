from django.utils import timezone
from .. import models as m


def test_is_paid():
    payment = m.Payment(paid_at=timezone.now())
    assert payment.is_paid is True

    payment2 = m.Payment()
    assert payment2.is_paid is False

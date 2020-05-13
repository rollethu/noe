from unittest.mock import Mock
import datetime as dt

import pytest

from billing import services as billing_services
from payments import services
from payments.models import Payment

DATE = dt.datetime(2020, 1, 1, 12)
OTHER_DATE = dt.datetime(2020, 1, 1, 13)


@pytest.mark.parametrize(
    "original_paid_at, all_data, raises_error",
    (
        (None, {}, False),
        (None, {"paid_at": None}, False),
        (None, {"paid_at": DATE}, False),
        (DATE, {}, False),
        (DATE, {"paid_at": None}, True),
        (DATE, {"paid_at": DATE}, False),
        (DATE, {"paid_at": OTHER_DATE}, True),
    ),
)
def test_validate_paid_at(original_paid_at, all_data, raises_error):
    payment = Payment(paid_at=original_paid_at)
    validate_func = lambda: services.validate_paid_at(payment, all_data)  # noqa
    if raises_error:
        pytest.raises(ValueError, validate_func)
    else:
        validate_func()


@pytest.mark.parametrize(
    "original_paid_at, all_data, should_send_invoice",
    (
        (None, {}, False),
        (None, {"paid_at": None}, False),
        (None, {"paid_at": DATE}, True),
        (DATE, {}, False),
        (DATE, {"paid_at": None}, False),
        (DATE, {"paid_at": DATE}, False),
        (DATE, {"paid_at": OTHER_DATE}, False),
    ),
)
def test_handle_paid_at(original_paid_at, all_data, should_send_invoice, monkeypatch):
    send_invoice_mock = Mock()
    monkeypatch.setattr(billing_services, "send_invoice", send_invoice_mock)

    payment = Payment(paid_at=original_paid_at)
    services.handle_paid_at(payment, all_data)

    if should_send_invoice:
        send_invoice_mock.assert_called_once()
    else:
        send_invoice_mock.assert_not_called()

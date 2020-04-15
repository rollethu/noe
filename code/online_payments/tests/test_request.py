import os
import pytest
from online_payments import simple_v2
from online_payments.exceptions import InvalidSignature


@pytest.mark.vcr()
def test_start_payment_request():
    total = 300
    order_ref = "101010515680292482600"

    res = simple_v2.start_payment_request(
        merchant=os.environ["SIMPLE_MERCHANT"],
        secret_key=os.environ["SIMPLE_SECRET_KEY"],
        customer_email="customer@gmail.com",
        order_ref=order_ref,
        total=total,
        callback_url="https://noe.rollet.app",
    )

    assert res.payment_url.startswith("https://")
    assert res.total == total
    assert res.orderRef == order_ref
    assert res.transaction_id != order_ref
    assert res.salt is not None


@pytest.mark.vcr()
def test_invalid_signature(vcr_cassette, vcr):
    vcr_cassette.responses[0]["headers"]["signature"] = "invalidsignature"
    with pytest.raises(InvalidSignature):
        simple_v2.start_payment_request(
            merchant=os.environ["SIMPLE_MERCHANT"],
            secret_key=os.environ["SIMPLE_SECRET_KEY"],
            customer_email="customer@gmail.com",
            order_ref="12345",
            total=300,
            callback_url="https://noe.rollet.app",
        )

import os
import pytest
from online_payments.simple_v2 import start_payment_request


@pytest.mark.vcr()
def test_start_payment_request():
    total = 300
    order_ref = "101010515680292482600"

    res = start_payment_request(
        merchant_id=os.environ["SIMPLE_MERCHANT_ID"],
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

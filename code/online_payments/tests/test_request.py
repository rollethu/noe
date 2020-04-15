import json
import os
import pytest
from online_payments import simple_v2
from online_payments.exceptions import InvalidSignature


def _remove_merchant_form_body(request):
    request_body = json.loads(request.body)
    if "merchant" in request_body:
        request_body["merchant"] = "S111111"

    request.body = json.dumps(request_body)
    return request


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "before_record_request": _remove_merchant_form_body,
    }


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

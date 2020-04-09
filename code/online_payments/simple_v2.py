import base64
import datetime as dt
import json
import hashlib
import hmac
import secrets
import requests

from . import exceptions


BASE_URL = "https://sandbox.simplepay.hu/payment/v2/start"


def get_payment_url(secret_key, customer_email, transaction_id, total):
    request_data = make_request_data(customer_email, transaction_id, total)
    json_request_data = make_json_request_data(request_data)
    signature = get_signature(json_request_data, secret_key)

    # `requests`'s default json dumping would keep whitespaces
    # Data sent in request and used for generating signature must match
    headers = {"Signature": signature, "Content-Type": "application/json"}
    rv = requests.post(BASE_URL, json_request_data, headers=headers)
    return rv.json()["paymentUrl"]


def make_request_data(
    merchant_id,
    transaction_id,
    total,
    callback_url,
    customer_email,
    currency="HUF",
    timeout_in_minutes=10,
):
    now = dt.datetime.utcnow()
    timeout_date = now + dt.timedelta(minutes=timeout_in_minutes)
    timeout_string = timeout_date.isoformat()

    return {
        "salt": secrets.token_urlsafe(32),
        "merchant": merchant_id,
        "orderRef": str(transaction_id),
        "currency": currency,
        "customerEmail": customer_email,
        "language": "HU",
        "sdkVersion": "SimplePayV2.1_Payment_PHP_SDK_2.0.7_190701:dd236896400d7463677a82a47f53e36e",
        "methods": ["CARD"],
        "total": str(total),
        "timeout": timeout_string,
        "url": callback_url,
        "invoice": {
            "name": "SimplePay V2 Tester",
            "company": "",
            "country": "hu",
            "state": "",
            "city": "",
            "zip": "",
            "address": "",
            "address2": "",
            "phone": "",
        },
    }


def make_json_request_data(request_data):
    # Simple expects compact json message with no "unnecessary whitespaces".
    return json.dumps(request_data, separators=[",", ":"])


def get_signature(json_data, secret_key):
    hmac_digest = hmac.new(
        secret_key.encode(), json_data.encode(), hashlib.sha384,
    ).digest()
    return base64.b64encode(hmac_digest).decode()

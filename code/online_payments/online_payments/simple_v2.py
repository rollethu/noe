import base64
import datetime as dt
from dataclasses import dataclass
import json
import hashlib
import hmac
import string
import secrets
import requests
from importlib import metadata
from dateutil.parser import parse as dateutil_parse
from . import exceptions

START_PAYMENT_URL = "https://sandbox.simplepay.hu/payment/v2/start"
# metadata.version works only when the package is installed, see:
# https://docs.python.org/3/library/importlib.metadata.html
SDK_VERSION = "Rollet online-payments " + metadata.version("online-payments")


@dataclass
class StartPaymentResponse:
    salt: str  # 32 character long random string
    merchant: str  # SimplePay account, in which the transaction has been created
    orderRef: str  # same as orderRef in start request
    currency: str  # same as currency in start request
    transaction_id: str  # created SimplePay transaction ID
    timeout: dt.datetime  # time limit until payment can be started
    total: float  # summary of the transaction
    payment_url: str  # URL where we need to redirect the user


def start_payment_request(
    *,
    merchant_id,
    secret_key,
    customer_email,
    order_ref,
    total,
    currency="HUF",
    callback_url,
    timeout_minutes=10,
):
    request = _make_request(
        merchant_id,
        customer_email,
        order_ref,
        total,
        currency,
        callback_url,
        timeout_minutes,
    )
    # Simple expects compact json message with no "unnecessary whitespaces".
    json_request = json.dumps(request, separators=[",", ":"])
    signature = _get_signature(json_request, secret_key)

    # `requests`'s default json dumping would keep whitespaces
    # Data sent in request and used for generating signature must match
    headers = {"Signature": signature, "Content-Type": "application/json"}
    res = requests.post(START_PAYMENT_URL, json_request, headers=headers)
    json_res = res.json()

    return StartPaymentResponse(
        salt=json_res["salt"],
        merchant=json_res["merchant"],
        orderRef=json_res["orderRef"],
        currency=json_res["currency"],
        transaction_id=json_res["transactionId"],
        timeout=dateutil_parse(json_res["timeout"]),
        total=json_res["total"],
        payment_url=json_res["paymentUrl"],
    )


def _make_request(
    merchant_id,
    customer_email,
    order_ref,
    total,
    currency,
    callback_url,
    timeout_minutes,
):
    now = dt.datetime.utcnow()
    timeout_date = now + dt.timedelta(minutes=timeout_minutes)
    timeout_date = timeout_date.replace(microsecond=0, tzinfo=dt.timezone.utc)
    timeout_string = timeout_date.isoformat()

    return {
        "salt": _random_string(32),
        "merchant": merchant_id,
        "orderRef": str(order_ref),
        "currency": currency,
        "customerEmail": customer_email,
        "language": "HU",
        "sdkVersion": SDK_VERSION,
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


def _random_string(n=32):
    """Generate a cryptographycally secure n-length random string
    containing printable characters, selected from lower- and upper-case
    ASCII letters, digits, punctuation and whitespace.
    """
    # https://docs.python.org/3/library/secrets.html#recipes-and-best-practices
    return "".join(secrets.choice(string.printable) for _ in range(n))


def _get_signature(json_data, secret_key):
    hmac_digest = hmac.digest(secret_key.encode(), json_data.encode(), hashlib.sha384)
    return base64.b64encode(hmac_digest).decode()

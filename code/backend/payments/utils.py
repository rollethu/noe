from . import models as m


def create_payments_and_transactions_for_appointment(appointment):
    payments = []
    for seat in appointment.seats:
        payment = m.Payment.objects.create(
            seat=seat, amount=1000, currency="HUF", payment_method_type=m.Payment.PAYMENT_METHOD_TYPE_SIMPLEPAY
        )
        payments.append(payment)
    m.Payment.objects.bulk_create(payments)
    total = sum(p.amount for p in payments)
    transaction = m.Transaction.objects.create(amount=total, payment=None,)  # TODO: Figure out which payment to use
    return payments, [transaction]


def update_transaction_with_simplepay_request(back_body, transaction):
    transaction.external_reference_id = back_body.order_id
    transaction.save()

    error = back_body.status_code != 0

    if not error and not back_body.status_code.isdigit():
        raise RuntimeError("Unexpected SimplePay response: {}".format(back_body.query_params))

    if error:
        transaction.status = transaction.STATUS_REJECTED
    else:
        transaction.status = transaction.STATUS_WAITING_FOR_AUTHORIZATION
    transaction.save()

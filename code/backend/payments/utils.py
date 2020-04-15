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

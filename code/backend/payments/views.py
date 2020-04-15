from django.conf import settings
from django.shortcuts import get_object_or_404, render
from online_payments import simple_v2
from rest_framework import viewsets

from . import models as m
from . import serializers as s
from . import utils as u


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = m.Payment.objects.all()
    serializer_class = s.PaymentSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = m.Transaction.objects.all()
    serializer_class = s.TransactionSerializer


def initiate_online_payment_view(request, appointment_pk):
    appointment = get_object_or_404(m.Appointment, pk=appointment_pk)
    payments, transactions = u.create_payments_and_transactions_for_appointment(appointment)
    transaction = transactions[0]
    simple_response = simple_v2.start_payment_request(
        merchant=settings.SIMPLEPAY_MERCHANT_ID,
        secret_key=settings.SIMPLEPAY_SECRET_KEY,
        customer_email=appointment.email,
        order_ref=transaction.pk,
        total=transaction.amount,
    )
    context = {"simple_url": simple_response.payment_url}
    return render(request, "simple-post-form.html", context=context)

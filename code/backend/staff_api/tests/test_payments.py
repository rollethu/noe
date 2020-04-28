import pytest
from rest_framework.reverse import reverse

from staff_api.serializers import PaymentSerializer


@pytest.mark.django_db
def test_payment_fields(factory, payment):
    payment.proof_number = "ASD"
    payment.save()

    request = factory.get(reverse("staff-payment-detail", kwargs={"pk": payment.pk}))
    serializer = PaymentSerializer(payment, context={"request": request})
    assert serializer.data["proof_number"] == "ASD"

from rest_framework import serializers

from . import models as m


class BillingDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = m.BillingDetail
        fields = [
            "appointment",
            "company_name",
            "country",
            "address_line1",
            "address_line2",
            "post_code",
            "state",
            "city",
            "tax_number",
        ]

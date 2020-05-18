from rest_framework import serializers

from . import models as m


class BillingDetailSerializer(serializers.HyperlinkedModelSerializer):
    is_company = serializers.BooleanField(write_only=True)

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
            "is_company",
        ]
        extra_kwargs = {"tax_number": {"required": False}}

from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from . import models as m


class BillingDetailSerializer(serializers.HyperlinkedModelSerializer):
    is_company = serializers.BooleanField(write_only=True, default=False)

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
        extra_kwargs = {"tax_number": {"required": False, "allow_blank": True}}

    def create(self, validated_data):
        is_company = validated_data.pop("is_company", False)
        if is_company and not validated_data.get("tax_number"):
            raise ValidationError({"tax_number": _("This field is required.")})
        return super().create(validated_data)
